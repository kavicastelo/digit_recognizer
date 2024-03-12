import numpy as np
from PIL import Image
from io import BytesIO
import webview
import tensorflow as tf
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

model = tf.keras.models.load_model('data_recognizer.h5')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files['image']
        img_array = preprocess_image(file.read())
        digit = predict_digit(model, img_array)

        return jsonify({'digit': int(digit)})

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'error_message': error_message})


def preprocess_image(img_data):
    img = Image.open(BytesIO(img_data))
    img = img.resize((28, 28))
    img_array = np.array(img.convert('L'))
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array


def predict_digit(model, img_array):
    img_array_flat = img_array.flatten()
    predictions = model.predict(np.array([img_array_flat]))
    digit = np.argmax(predictions)
    return digit


if __name__ == '__main__':
    webview.create_window('Digit Recognizer', app, width=800, height=600)
    webview.start()
