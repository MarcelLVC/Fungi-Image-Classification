from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import cv2
import numpy as np
import base64
import os
from skimage.feature import graycomatrix, graycoprops, local_binary_pattern

app = Flask(__name__)
CORS(app)

MODEL_PATH = os.path.join(os.getcwd(), 'scripts', 'rf_defungi.joblib')

# Load model 
try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print(f"Model loaded from {MODEL_PATH}")
    else:
        model = joblib.load(os.path.join(os.getcwd(), 'scripts', 'best_xgb_defungi.joblib'))
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

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

@app.route('/classify', methods=['POST'])
def classify():
    if not model:
        return jsonify({"error": "Model not loaded"}), 500
        
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
        
        features = extract_all_features(img)
        features = features.reshape(1, -1)
        
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        confidence = max(probabilities)
        
        # Class mapping
        classes = ["Candida Albicans", "Aspergillus Niger", "Trichophyton Rubrum", 
                   "Trichophyton Mentagrophytes", "Epidermophyton Floccosum"]
        
        try:
            pred_class = classes[int(prediction)]
        except:
            pred_class = "Unable to Classify Species"

        return jsonify({
            "class": pred_class,
            "confidence": float(confidence)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
