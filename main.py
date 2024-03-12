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
    return render_template('templates/templates/index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get image file from the HTML form
        file = request.files['image']
        img_array = preprocess_image(file.read())

        # Flatten the image data
        img_array_flat = img_array.flatten()

        # Make predictions
        predictions = model.predict(np.array([img_array_flat]))

        # Print raw predictions for debugging
        print("Raw Predictions:", predictions)

        digit = np.argmax(predictions)

        return render_template('templates/templates/index.html', digit=int(digit))

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template('templates/templates/index.html', error_message=error_message)


def preprocess_image(img_data):
    # Convert bytes to PIL Image
    img = Image.open(BytesIO(img_data))

    # Resize and normalize the image
    img = img.resize((28, 28))
    img_array = np.array(img.convert('L'))  # Convert to grayscale

    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    return img_array


if __name__ == '__main__':
    app.run(debug=True)
