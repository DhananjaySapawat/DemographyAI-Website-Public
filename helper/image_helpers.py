from helper.models import load_model, extract_face, extract_face_features
import cv2
import base64
from flask import jsonify
import numpy as np

def extract_face_data(cv2_image, is_webcam=False):
    frontend_data = []
    backend_data = []
    model = load_model(with_age = True)
    for face_image in extract_face(cv2_image, is_webcam):
        age, age_range, gender, ethnicity, emotion = extract_face_features(model, face_image)

        _, buffer = cv2.imencode('.jpg', face_image)
        encoded_face_image = base64.b64encode(buffer).decode('utf-8')
        raw_face_image_data = buffer.tobytes()

        frontend_data.append({
            'image': encoded_face_image,
            'age': age_range,
            'gender': gender,
            'ethnicity': ethnicity,
            'emotion': emotion
        })

        backend_data.append({
            'image': raw_face_image_data,
            'age': age,
            'age_range': age_range,
            'gender': gender,
            'ethnicity': ethnicity,
            'emotion': emotion
        })
    
    frontend_response = jsonify({'body': frontend_data})
    processed_image = convert_cv_to_buffer(cv2_image)
    
    backend_response = {
        "original_image": processed_image,
        "faces": backend_data
    }

    return frontend_response, backend_response

def convert_canvas_to_cv(image_data):
    image_data = image_data.split(",")[1]  # Remove base64 metadata
    img_bytes = base64.b64decode(image_data)
    img_array = np.frombuffer(img_bytes, np.uint8)
    return cv2.imdecode(img_array, cv2.IMREAD_COLOR)

def process_uploaded_image(file):
    file_bytes = np.frombuffer(file.read(), np.uint8)
    return cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

def convert_cv_to_buffer(image):
    _, encoded_image = cv2.imencode('.jpg', image)
    return encoded_image.tobytes()

def convert_cv_to_frontend_buffer(image):
    _, encoded_image = cv2.imencode('.jpg', image)
    return base64.b64encode(encoded_image).decode('utf-8')

