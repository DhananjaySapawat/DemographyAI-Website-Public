from helper.models import load_model, extract_face_features
import cv2 
import os
import tempfile
from helper.cloud_functions import upload_video_to_cloud
from helper.face_detection.yunet import extract_face_coordinates_upload

def get_labels(model, frame):
    current_labels = []
    for (x, y, w, h) in extract_face_coordinates_upload(frame):
        face = frame[y:y + h, x:x + w]
        age_range, gender, ethnicity, emotion = extract_face_features(model, face)
        current_labels.append((x, y, x + w, y + h, age_range, gender, ethnicity, emotion))

    return current_labels

def write_face_labels(frame, detected_labels):

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    thickness = 2
    text_height = 20  
    bg_color = (35,102,11)

    for (x1, y1, x2, y2, age, gender, ethnicity, emotion) in detected_labels:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        annotations = [f'Age: {age}',f'Gender: {gender}',f'Ethnicity: {ethnicity}',f'Emotion: {emotion}']

        for i, text in enumerate(annotations):
            top_left = (x1, y2 + i * text_height)
            bottom_right = (x2, y2 + (i + 1) * text_height)
            cv2.rectangle(frame, top_left, bottom_right, bg_color, cv2.FILLED)
            text_position = (x1 + 5, y2 + (i + 1) * text_height - 5)
            cv2.putText(frame, text, text_position, font, font_scale, (255, 255, 255), thickness)

def get_frame_stat(cap):
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return frame_rate, frame_width, frame_height, total_frames

def process_live_video(temp_file, processed_temp_file, progress):
    model = load_model(with_age = False)

    cap = cv2.VideoCapture(temp_file)
    frame_rate, frame_width, frame_height, total_frames = get_frame_stat(cap)
    fourcc = cv2.VideoWriter_fourcc(*'VP80')
    out = cv2.VideoWriter(processed_temp_file, fourcc, frame_rate, (frame_width, frame_height))

    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frames_to_process = 1
        detected_labels = []
        if frame_count % frames_to_process == 0:
            detected_labels = get_labels(model, frame)
            write_face_labels(frame, detected_labels)

        frame_count += 1
        progress["percent"] = int((frame_count / total_frames) * 100)
        out.write(frame)

    cap.release()
    out.release()

def process_upload_video(file_content, progress):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_file.close()  
    with open(temp_file.name, 'wb') as f:
        f.write(file_content) 

    processed_temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".webm")
    processed_temp_file.close()

    process_live_video(temp_file.name, processed_temp_file.name, progress)
    url = upload_video_to_cloud(processed_temp_file.name)

    os.remove(temp_file.name)
    os.remove(processed_temp_file.name)

    return url
 
