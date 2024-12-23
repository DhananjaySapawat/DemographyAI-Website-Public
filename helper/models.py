from helper.model_details import mapping, image_dimension, mean, std, model_path
import cv2 
from tflite_runtime.interpreter import Interpreter
import numpy as np 
from PIL import Image
import os
from helper.face_detection.yunet import extract_face_coordinates_upload, extract_face_coordinates_camera

def extract_face(frame, is_webcam=False):
    frame_faces = []
    if is_webcam:
        for (x, y, w, h) in extract_face_coordinates_camera(frame):
            frame_faces.append(frame[y:y + h, x:x + w])
    else:
        for (x, y, w, h) in extract_face_coordinates_upload(frame):
            frame_faces.append(frame[y:y + h, x:x + w])  
    return frame_faces

def transform_image(face_image):
    image = Image.fromarray(face_image.astype(np.uint8))
    image = image.resize((image_dimension, image_dimension), Image.BILINEAR)
    face_image = np.array(image, dtype=np.float32).transpose(2, 0, 1)
    face_image = (face_image / 255.0 - mean[:, None, None]) / std[:, None, None]
    face_image = np.expand_dims(face_image, axis=0)
    return face_image

def load_tflite_model(model_path):
    """Load TensorFlow Lite model and return its interpreter."""
    interpreter = Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter

def load_model(with_age=False):
    models = {key: load_tflite_model(path) for key, path in model_path.items()}
    if not with_age:
        models.pop("age", None)
    return models

def run_tflite_model(model, face_image):
    input_details = model.get_input_details()
    output_details = model.get_output_details()
    model.set_tensor(input_details[0]['index'], np.array(face_image, dtype=np.float32))
    model.invoke()
    output_data = model.get_tensor(output_details[0]['index'])
    return output_data

def extract_face_features(models, face_image):
    face_image = transform_image(face_image)
    
    age_range_logit = run_tflite_model(models['age_range'], face_image)
    age_label = np.argmax(age_range_logit, axis=1).item()
    age_range = mapping["age_range"][age_label]        

    gender_logit = run_tflite_model(models['gender'], face_image).item()
    gender_id = (1 / (1 + np.exp(-gender_logit)) > 0.5).astype(int)
    gender = mapping["gender"][gender_id] 
        
    ethnicity_logit = run_tflite_model(models['ethnicity'], face_image)
    ethnicity_id = np.argmax(ethnicity_logit, axis=1).item()
    ethnicity = mapping["ethnicity"][ethnicity_id]  

    emotion_logit = run_tflite_model(models['emotion'], face_image)
    emotion_id = np.argmax(emotion_logit, axis=1).item()
    emotion = mapping["emotion"][emotion_id] 

    if "age" in models.keys(): 
        age_logit = run_tflite_model(models['age'], face_image)
        age = str(int(age_logit.item()))
        return age, age_range, gender, ethnicity, emotion

    else:
        return age_range, gender, ethnicity, emotion

