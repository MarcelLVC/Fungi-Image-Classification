from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import cv2
import numpy as np
import base64
import os
import sys

from skimage.feature import graycomatrix, graycoprops, local_binary_pattern

app = Flask(__name__)
CORS(app)

# Feature extraction functions 
def extract_glcm_features(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    glcm = graycomatrix(gray, distances=[1], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4], 
                        levels=256, symmetric=True, normed=True)
    features = []
    props = ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']
    for prop in props:
        val = graycoprops(glcm, prop).mean()
        features.append(val)
    return np.array(features)

def extract_lbp_features(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    radius = 1
    n_points = 8 * radius
    lbp = local_binary_pattern(gray, n_points, radius, method='uniform')
    hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, n_points + 3), range=(0, n_points + 2))
    hist = hist.astype("float")
    hist /= (hist.sum() + 1e-7)
    return hist

def extract_hsv_features(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    bins = 8
    hist_h = cv2.calcHist([hsv], [0], None, [bins], [0, 180])
    hist_s = cv2.calcHist([hsv], [1], None, [bins], [0, 256])
    hist_v = cv2.calcHist([hsv], [2], None, [bins], [0, 256])
    cv2.normalize(hist_h, hist_h)
    cv2.normalize(hist_s, hist_s)
    cv2.normalize(hist_v, hist_v)
    return np.concatenate([hist_h.flatten(), hist_s.flatten(), hist_v.flatten()])

def extract_all_features(image):
    img = cv2.resize(image, (256, 256))
    feat_glcm = extract_glcm_features(img)
    feat_lbp = extract_lbp_features(img)
    feat_hsv = extract_hsv_features(img)
    return np.concatenate([feat_glcm, feat_lbp, feat_hsv])

model = None

def get_model():
    global model
    if model is None:
        # model
        model_path = os.path.join(os.getcwd(), 'scripts', 'rf_defungi.joblib')
        
        if not os.path.exists(model_path):
             model_path = os.path.join(os.getcwd(), 'scripts', 'best_xgb_defungi.joblib')
        
        if os.path.exists(model_path):
            model = joblib.load(model_path)
        else:
            raise FileNotFoundError(f"Model not found at {model_path}")
    return model

@app.route('/api/classify-py', methods=['POST'])
def classify():
    try:
        data = request.json
        image_data = data.get('image', '')
        
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({"error": "Invalid image"}), 400
        
        current_model = get_model()
        features = extract_all_features(img)
        features = features.reshape(1, -1)
        
        prediction = current_model.predict(features)[0]
        probabilities = current_model.predict_proba(features)[0]
        confidence = max(probabilities)

        classes = ["Candida Albicans", "Aspergillus Niger", "Trichophyton Rubrum", 
                   "Trichophyton Mentagrophytes", "Epidermophyton Floccosum"]
        
        try:
             pred_class = classes[int(prediction)]
        except:
             pred_class = "Unknown Class"

        return jsonify({
            "class": pred_class,
            "confidence": float(confidence),
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)