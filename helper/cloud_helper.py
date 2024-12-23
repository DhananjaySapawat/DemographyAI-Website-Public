from collections import defaultdict
from datetime import datetime
import random
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

def encrypt_password(password, key):
    key = key.ljust(32)[:32].encode('utf-8')
    cipher = AES.new(key, AES.MODE_ECB)
    ct_bytes = cipher.encrypt(pad(password.encode('utf-8'), AES.block_size))
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return ct

def decrypt_password(ct, key):
    key = key.ljust(32)[:32].encode('utf-8')
    ct = base64.b64decode(ct)
    cipher = AES.new(key, AES.MODE_ECB)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')

def create_password(length=12):
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = string.punctuation
    
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special_chars)
    ]
    
    all_chars = lowercase + uppercase + digits + special_chars
    password += random.choices(all_chars, k=length - 4)
    
    random.shuffle(password)
    return ''.join(password)

def create_username(email, exist_usernames):
    username = email.split('@')[0]  # Extract the base username from the email
    original_username = username
    counter = 1
    existing_usernames_set = {user["username"] for user in exist_usernames}
    while username in existing_usernames_set:
        username = f"{original_username}{counter}"
        counter += 1
    return username

def format_data(image_data, face_data):
    # Organize face data by face_image_id for quicker lookups
    face_data_by_image = defaultdict(list)
    for face_record in face_data:
        face_data_by_image[face_record["image_id"]].append({
            "face_url": face_record["face_url"],
            "age": face_record["age"],
            "age_range": face_record["age_range"],
            "gender": face_record["gender"],
            "ethnicity": face_record["ethnicity"],
            "emotion": face_record["emotion"]
        })

    # Format the data for each image
    formatted_data = []
    
    for image_record in image_data:
        image_face_data = face_data_by_image.get(image_record["id"], [])
        time_obj = datetime.strptime(image_record["time"], "%Y-%m-%dT%H:%M:%S.%f")
        formatted_data.append({
            "image_url": image_record["url"],
            "folder_name": image_record["upload_folder"],
            "time": time_obj,
            "date": time_obj.date(),
            "faces": image_record["faces"],
            "size" : image_record["size"],
            "face_data": image_face_data
        })
    return formatted_data
        
def get_filter_data(data, folder=None, date_size=None):
    if folder:
        data = [item for item in data if item['folder_name'] == folder.capitalize()]
    
    if date_size:
        if date_size == 'older':
            data = sorted(data, key=lambda x: x['time'], reverse=False)
        elif date_size == 'newer':
            data = sorted(data, key=lambda x: x['time'], reverse=True)
        elif date_size == 'size':
            data = sorted(data, key=lambda x: x['faces']) 
        elif date_size == 'face':
            data = sorted(data, key=lambda x: x['faces'], reverse=True)  
    return data

def get_encrpt_user_requests(user_requests, encryption_key):
    encrpt_user_requests = []
    for user_request in user_requests:
        user_request["password"] = decrypt_password(user_request["password"], encryption_key)
        encrpt_user_requests.append(user_request)
    return encrpt_user_requests