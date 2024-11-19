from tensorflow import keras
from PIL import Image, ImageOps
import numpy as np
import requests
from io import BytesIO
from app.constants import Constants


class TensorflowAI:
    _instance = None
    model = None
    class_names = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TensorflowAI, cls).__new__(cls)
            cls._instance.initModel()
        return cls._instance

    def initModel(self):
        # Load the model
        try:
            # Disable scientific notation for clarity
            np.set_printoptions(suppress=True)
            # Load the model
            self.model = keras.models.load_model(Constants.MODEL_TEACHABLE_MACHINE, compile=False)
            # Load the labels
            self.class_names = open(Constants.LABELS_TEACHABLE_MACHINE, "r").readlines()
        except Exception as e:
            print(f"Error loading model: {e}")

    def predict_image(self, urlImage):
        if not self.model:
            self.initModel()

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {Constants.API_TOKEN}'
        }

        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # Download the image from the URL
        response = requests.get(urlImage, headers=headers)
        image = Image.open(BytesIO(response.content)).convert("RGB")

        # Resize the image to be at least 224x224 and then crop from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

        # Turn the image into a numpy array
        image_array = np.asarray(image)

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # Predict using the model
        prediction = self.model.predict(data)
        # Create a list of dictionaries with class names and probabilities
        predictions = [{
            'className': self.class_names[index],
            'probability': "{:.6f}".format(prob)
        } for index, prob in enumerate(prediction[0])]

        sorted_predictions = sorted(predictions, key=lambda x: x['probability'], reverse=True)

        return sorted_predictions
