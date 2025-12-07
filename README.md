# Fungal-Infection-Image-Classification

npm install
npm install concurrently --save-dev

# buat coba test flask server
python scripts/classify_fungi.py --model scripts/rfmodel_n100.joblib --server

# bisa buat jalanin npm sama flask barengan 
npm run dev:all

# requirement nya
pip install opencv-python numpy scikit-image scikit-learn joblib flask flask-cors  