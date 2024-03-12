import numpy as np


def predict_digit(model, img_array):
    # Flatten the image data
    img_array_flat = img_array.flatten()

    # Make predictions
    predictions = model.predict(np.array([img_array_flat]))

    # Print raw predictions for debugging
    print("Raw Predictions:", predictions)

    digit = np.argmax(predictions)

    return digit
