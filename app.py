from image_processing import preprocess_image
from prediction import predict_digit

from flask import Flask, render_template, request, jsonify
import numpy as np
import tensorflow as tf
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Load the model using joblib
model = tf.keras.models.load_model('data_recognizer.h5')


@app.route('/')
def home():
    return render_template('templates/index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get image file from the HTML form
        file = request.files['image']
        img_array = preprocess_image(file.read())

        # Make predictions using a separate module
        digit = predict_digit(model, img_array)

        return jsonify({'digit': int(digit)})

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'error_message': error_message})


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
