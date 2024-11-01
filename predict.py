import pickle
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

# Load the model
with open('model.pkl', 'rb') as file:
    model_data = pickle.load(file)

# Reconstruct the model
model = model_from_json(model_data["architecture"])
model.set_weights(model_data["weights"])

# Compile the model (necessary for making predictions)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

def predict(image_path):
    # Preprocess the image
    img = load_img(image_path, target_size=(150, 150))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array /= 255.0  # Normalize to [0, 1]

    # Make a prediction
    prediction = model.predict(img_array)
    
    # Return the predicted class
    return "Vehicles" if prediction[0][0] > 0.5 else "Non-Vehicles"
