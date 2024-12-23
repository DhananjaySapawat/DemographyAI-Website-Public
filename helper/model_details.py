import numpy as np 

gender_mapping = {0: 'Female', 1: 'Male'}
ethnicity_mapping = {0: 'Asian', 1: 'Black', 2: 'Indian', 3: 'Others', 4: 'White'}
emotion_mapping = {0: 'Anger', 1: 'Contempt', 2: 'Disgust', 3: 'Fear', 4: 'Happy', 5: 'Neutral', 6: 'Sad', 7: 'Surprise'}
idx_to_age_range = {0: '0-9', 1: '10-19', 2: '20-24', 3: '25-29', 4: '30-34', 5: '35-39', 6: '40-44', 7: '45-54', 8: '55-116'}

mapping = {
    "age_range" : idx_to_age_range,
    "gender" : gender_mapping,
    "ethnicity" : ethnicity_mapping,
    "emotion" : emotion_mapping
}

image_dimension = 200
mean = np.array([0.485, 0.456, 0.406]) 
std = np.array([0.229, 0.224, 0.225])

model_path = {
    "age" : "tflite_models/age_model.tflite",
    "age_range" : "tflite_models/age_range_model.tflite",
    "gender" :"tflite_models/gender_model.tflite",
    "ethnicity" :"tflite_models/ethnicity_model.tflite",
    "emotion" : "tflite_models/emotion_model.tflite"
}


