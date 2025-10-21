from flask import Flask, request, jsonify, render_template
import numpy as np
import tensorflow as tf
import cv2
import os
import ssl
from werkzeug.utils import secure_filename
import importlib
_tfi = None
try:
    _tfi = importlib.import_module('tensorflow.keras.preprocessing.image')
    load_img = _tfi.load_img
    img_to_array = _tfi.img_to_array
    save_img = _tfi.save_img
except Exception:
    # Fall back to a tiny PIL-based implementation for environments
    # where tensorflow isn't available to the static analyzer/runtime.
    from PIL import Image
    def load_img(path, target_size=None):
        img = Image.open(path).convert('RGB')
        if target_size:
            img = img.resize(target_size)
        return img

    def img_to_array(img):
        return np.array(img)

    def save_img(path, arr):
        img = Image.fromarray(arr.astype('uint8'))
        img.save(path)

ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

MODEL_DIR = os.path.join('.', 'model')
MODEL_PATH = os.path.join(MODEL_DIR, 'model.h5')
MODEL_URL = os.environ.get('MODEL_URL')

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

if not os.path.exists(MODEL_PATH):
    if MODEL_URL:
        # download model from URL into model path
        try:
            import requests
            print(f'Downloading model from {MODEL_URL} to {MODEL_PATH}...')
            with requests.get(MODEL_URL, stream=True) as r:
                r.raise_for_status()
                with open(MODEL_PATH, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            print('Model downloaded successfully.')
        except Exception as e:
            print('Failed to download model:', e)
    else:
        print('No model found at', MODEL_PATH, 'and MODEL_URL not set. Loading will fail unless model is present.')

model = tf.keras.models.load_model(MODEL_PATH)

ALLOWED_EXTENSIONS = {'png','jpg','jpeg','bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(file_path):
    """
    Preprocesses the image for model predicition.

    Args:
        file_path (str): Path to the image file.

    Return:
        numpy.ndarray: Preprocessed image ready for predicition.
    """
    #Load the image
    img = load_img(file_path, target_size=(64, 64))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed types are png, jpg, jpeg'}), 400
    
    #Save the uploaded file
    filename = secure_filename(file.filename)
    file_path = os.path.join('uploads', filename)
    file.save(file_path)

    try:
        img = preprocess_image(file_path)

        predictions = model.predict(img)
        predicted_class = int(np.argmax(predictions[0]))
        print('predicted_class is: ', predicted_class)

        class_names = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        predicted_label = class_names[predicted_class]


        return jsonify({
            'predicted_class': predicted_class,
            'predicted_label': predicted_label,
            'confidence': float(np.max(predictions[0]))
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)


