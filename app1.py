import streamlit as st
import joblib
import cv2
import numpy as np
from skimage.feature import graycomatrix, graycoprops, local_binary_pattern
from PIL import Image
import os

# --- Page Config ---
st.set_page_config(
    page_title="FungiScope",
    layout="wide"
)

# --- Custom CSS for Fonts & Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&display=swap');

    /* Apply Display Font to Titles */
    h1, h2, h3 {
        font-family: 'Oswald', sans-serif !important;
        color: #1b5e20; /* Dark Green Title */
    }
    
    /* Sans Serif for normal text (Streamlit default, but ensuring black) */
    p, div, label {
        font-family: 'Source Sans Pro', sans-serif;
        color: #000000;
    }

    /* Green Buttons */
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }

    /* Result Card Styling */
    .result-box {
        padding: 20px;
        background-color: #e8f5e9; /* Light Green Background */
        border-left: 5px solid #2e7d32;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# feature extraction
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

# load model
@st.cache_resource
def load_model():
    possible_paths = [
        "scripts/rf_defungi.joblib", 
        "rf_defungi.joblib", 
        "scripts/best_xgb_defungi.joblib"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return joblib.load(path)
    return None

model = load_model()

page = st.sidebar.radio("Go to", ["Classify Image", "About Our Model"])

if page == "Classify Image":
    st.title("FungiScope")
    st.write("Microscopic Fungi Classifier, Upload a microscopic image to detect the fungi species.")

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("1. Upload Image")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Microscopic Image', use_container_width=True)
            
            # Convert for OpenCV
            img_array = np.array(image.convert('RGB'))
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    with col2:
        st.subheader("2. Classification Results")
        
        if uploaded_file is None:
            st.info("👈 Please upload an image to see the results here.")
        else:
            if st.button('Analyze Image', use_container_width=True):
                if model is None:
                    st.error("Model not found! Check your file path.")
                else:
                    with st.spinner('Extracting Features & Predicting...'):
                        try:
                            # Prediction Logic
                            features = extract_all_features(img_bgr)
                            features = features.reshape(1, -1)
                            prediction = model.predict(features)[0]
                            probabilities = model.predict_proba(features)[0]
                            confidence = max(probabilities)

                            # Classes
                            classes = ["Candida Albicans", "Aspergillus Niger", "Trichophyton Rubrum", 
                                       "Trichophyton Mentagrophytes", "Epidermophyton Floccosum"]
                            
                            try:
                                pred_class = classes[int(prediction)]
                            except:
                                pred_class = "Unknown Class"

                            # Display Results
                            st.markdown(f"""
                                <div class="result-box">
                                    <h2 style="margin:0; color:#1b5e20;">{pred_class}</h2>
                                    <p style="margin:0; font-size:18px;">Confidence Score: <b>{confidence*100:.1f}%</b></p>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # Bar Chart
                            st.write("Confidence Level:")
                            st.progress(float(confidence), text=f"{confidence*100:.1f}%")

                            # Detailed Probabilities Expander
                            with st.expander("See details for all classes"):
                                for i, class_name in enumerate(classes):
                                    prob = probabilities[i]
                                    st.write(f"**{class_name}**")
                                    st.progress(float(prob), text=f"{prob*100:.1f}%")

                        except Exception as e:
                            st.error(f"Error: {e}")

# about model page
elif page == "About Our Model":
    st.title("🧠 About the Model")
    
    st.markdown("""
    ### Machine Learning Algorithms
    We utilize powerful ensemble learning methods to classify fungi species based on texture and color features.
    """)

    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("""
        #### 🌲 Random Forest
        Random Forest is an ensemble learning method that constructs a multitude of decision trees during training. 
        * **Why we use it:** It handles high-dimensional data well and is robust against overfitting.
        * **Outcome:** It outputs the class that is the mode of the classes (classification) of the individual trees.
        """)
        
    with col_b:
        st.markdown("""
        #### 🚀 XGBoost
        XGBoost (Extreme Gradient Boosting) is an optimized distributed gradient boosting library.
        * **Why we use it:** It is highly efficient, flexible, and portable. It usually provides state-of-the-art results for tabular data.
        * **Mechanism:** It builds trees sequentially, where each new tree corrects errors made by the previous ones.
        """)
    
    st.divider()
    
    st.markdown("### 🔍 Feature Extraction Techniques")
    st.write("Before feeding images into the model, we extract numerical data using these three techniques:")

    st.info("""
    **1. GLCM (Gray-Level Co-occurrence Matrix)**
    * **What it does:** Analyzes the texture of the image.
    * **Features:** Contrast, Dissimilarity, Homogeneity, Energy, Correlation, ASM.
    * **Application:** Helps distinguish between rough and smooth fungal textures.
    """)

    st.info("""
    **2. LBP (Local Binary Pattern)**
    * **What it does:** A powerful texture descriptor that thresholds each pixel against its neighbors.
    * **Application:** Captures fine-grained details and micro-patterns on the fungi surface.
    """)

    st.info("""
    **3. HSV Color Histogram**
    * **What it does:** Converts the image from RGB to HSV (Hue, Saturation, Value) color space.
    * **Application:** Since fungi species often have distinct colors (e.g., Aspergillus Niger is black/dark brown), color features are crucial for accurate classification.
    """)