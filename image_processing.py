import numpy as np
from PIL import Image
from io import BytesIO


def preprocess_image(img_data):
    # Convert bytes to PIL Image
    img = Image.open(BytesIO(img_data))

    # Resize and normalize the image
    img = img.resize((28, 28))
    img_array = np.array(img.convert('L'))  # Convert to grayscale

    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    return img_array
