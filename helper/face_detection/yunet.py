import cv2
from fdlite import FaceDetection, FaceDetectionModel

FACE_DETECTOR_MODEL_PATH = "helper/face_detection/yunet_n_640_640.onnx"

def scale_coordinates(face_coordinates, scale_width, scale_height):
    x, y, w, h = face_coordinates[:4]
    return int(x * scale_width), int(y * scale_height), int(w * scale_width), int(h * scale_height)

def extract_face_coordinates_upload(image):
    scale = max(image.shape[1] / 1280, image.shape[0] / 1280)
    width, height = image.shape[1], image.shape[0]
    if scale <= 1:
        scale = 1
    else:
        width, height = int(width / scale), int(height / scale)

    face_detector = cv2.FaceDetectorYN.create(FACE_DETECTOR_MODEL_PATH, "", (width, height))
    resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    _, detected_faces = face_detector.detect(resized_image)
    if detected_faces is None:
        return []
    return [scale_coordinates(face, scale, scale) for face in detected_faces]


def extract_face_coordinates_camera(image):
    face_cord = []
    detect_faces = FaceDetection(model_type=FaceDetectionModel.BACK_CAMERA)
    faces = detect_faces(image)
    for face in faces:
        box = face.bbox
        x, y, w, h = box.xmin, box.ymin, box.xmax - box.xmin, box.ymax - box.ymin
        face_cord.append((int(x * image.shape[1]) - 20, int(y * image.shape[0]) - 70, int(w * image.shape[1]) + 40, int(h * image.shape[0]) + 80))
    return face_cord