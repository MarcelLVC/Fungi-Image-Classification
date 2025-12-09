import cv2
import numpy as np
from skimage.feature import graycomatrix, graycoprops, local_binary_pattern
import joblib
import argparse
import sys
import os

# feat ex

def extract_glcm_features(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Calculate GLCM (distance 1 pixel, angles 0, 45, 90, 135 degrees)
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


# classification model 

def load_model(model_path):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    return joblib.load(model_path)

def classify_image(image_path, model_path):
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    # Load model
    model = load_model(model_path)
    
    # Extract features
    features = extract_all_features(img)
    features = features.reshape(1, -1)
    
    # Predict
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    confidence = max(probabilities)
    
    return {
        "class": prediction,
        "confidence": float(confidence),
        "probabilities": {cls: float(prob) for cls, prob in zip(model.classes_, probabilities)}
    }


# flask server

def run_server(model_path, host='0.0.0.0', port=5000):
    """Run Flask server for API integration"""
    try:
        from flask import Flask, request, jsonify
        from flask_cors import CORS
        import base64
    except ImportError:
        print("Please install Flask and flask-cors: pip install flask flask-cors")
        sys.exit(1)
    
    app = Flask(__name__)
    CORS(app)
    
    # Load model once at startup
    model = load_model(model_path)
    
    @app.route('/classify', methods=['POST'])
    def classify():
        try:
            data = request.json
            image_data = data.get('image', '')
            
            # Decode base64 image
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                return jsonify({"error": "Invalid image"}), 400
            
            # Extract features
            features = extract_all_features(img)
            features = features.reshape(1, -1)
            
            # Predict
            prediction = model.predict(features)[0]
            probabilities = model.predict_proba(features)[0]
            confidence = max(probabilities)
            
            # Return feature counts for UI
            feat_glcm = extract_glcm_features(cv2.resize(img, (256, 256)))
            feat_lbp = extract_lbp_features(cv2.resize(img, (256, 256)))
            feat_hsv = extract_hsv_features(cv2.resize(img, (256, 256)))

            if(prediction==0):
                prediction = "Candida Albicans"
            elif(prediction==1):
                prediction = "Aspergillus Niger"
            elif(prediction==2):
                prediction = "Trichophyton Rubrum"
            elif(prediction==3):
                prediction = "Trichophyton Mentagrophytes"
            elif(prediction==4):
                prediction = "Epidermophyton Floccosum"
            else:
                prediction = "Unable to Classify Species"
            
            return jsonify({
                "class": prediction,
                "confidence": float(confidence),
                "features": {
                    "glcm": feat_glcm.tolist(),
                    "lbp": feat_lbp.tolist(),
                    "hsv": feat_hsv.tolist()
                }
            })
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    print(f"Starting server on http://{host}:{port}")
    app.run(host=host, port=port, debug=False)


# main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fungi Classification Tool")
    parser.add_argument("--image", type=str, help="Path to image file")
    parser.add_argument("--model", type=str, default="model.joblib", help="Path to model file")
    parser.add_argument("--server", action="store_true", help="Run as Flask server")
    parser.add_argument("--port", type=int, default=5000, help="Server port")
    
    args = parser.parse_args()
    
    if args.server:
        run_server(args.model, port=args.port)
    elif args.image:
        result = classify_image(args.image, args.model)
        print(f"\nClassification Result:")
        print(f"  Class: {result['class']}")
        print(f"  Confidence: {result['confidence']:.2%}")
        print(f"\nProbabilities:")
        for cls, prob in result['probabilities'].items():
            print(f"  {cls}: {prob:.2%}")
    else:
        parser.print_help()
