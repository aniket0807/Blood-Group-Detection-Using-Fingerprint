This project uses Deep Learning (CNN) to detect a person’s blood group from a fingerprint image.
A trained TensorFlow/Keras model classifies fingerprint images into 8 blood group classes:

A+, A−, B+, B−, AB+, AB−, O+, O−

The project includes:

A trained deep learning model (model.h5)

A Flask web application for easy testing

A clean front-end (HTML + CSS + JS) interface

API endpoint (/predict) for programmatic access

🚀 Features

✅ Predict blood group from uploaded fingerprint image
✅ User-friendly web interface
✅ REST API for integration with other systems
✅ 97% classification accuracy
✅ Responsive UI with real-time preview
✅ Confusion matrix for model evaluation

🧠 Model Information

Framework: TensorFlow / Keras

Architecture: CNN (Convolutional Neural Network)

Input size: 64×64 pixels

Accuracy: ~97%

Dataset: Fingerprint images labeled with blood groups

🖥️ Tech Stack
Area	Technology
Frontend	HTML5, CSS3, JavaScript
Backend	Flask (Python)
Model	TensorFlow / Keras
Tools	OpenCV, NumPy
Testing	Postman
Version Control	Git, GitHub
⚙️ Setup & Run
1️⃣ Clone the Repository
git clone https://github.com/<your-username>/blood-group-detection.git
cd blood-group-detection

2️⃣ Create a Virtual Environment
python -m venv venv
venv\Scripts\activate       # On Windows
source venv/bin/activate    # On macOS/Linux

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the Flask App
python app.py


Then open your browser and go to:

http://127.0.0.1:5000/

🧩 API Usage (for developers)
Endpoint
POST /predict

Parameters
Name	Type	Description
file	File	Fingerprint image (.png, .jpg, .jpeg, .bmp)
Example Response
{
  "predicted_class": 3,
  "predicted_label": "B+",
  "confidence": 0.974
}

📊 Model Evaluation

The CNN model achieved 97% overall accuracy.
Below is the confusion matrix from validation:

⭐ How to Contribute

Fork the repo

Create a new branch (feature/your-feature)

Commit your changes

Push to your branch and open a Pull Request

📝 License

This project is open source under the MIT License.
