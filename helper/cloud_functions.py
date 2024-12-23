from supabase import create_client, Client
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from dotenv import load_dotenv
import os
from helper.cloud_helper import create_password, create_username, format_data, encrypt_password, decrypt_password

load_dotenv()
cloud_name = os.getenv("CLOUD_NAME")
api_key = os.getenv("API_KEY")
Api_secret = os.getenv("API_SECRET")

supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")

encryption_key = os.getenv("ENCRYPTION_KEY")

# Configuration       
cloudinary.config( 
    cloud_name = cloud_name, 
    api_key = api_key, 
    api_secret = Api_secret, 
    secure=True
)

supabase: Client = create_client(supabase_url, supabase_key)

def insert_user_data(upload_folder, url, size, face_data):
    folder_mapping = {"Uploaded Images": "Upload", "Snapshot Images": "Snapshot"}
    try:
        # Insert image data into the 'image_data' table
        image_data = {
            "upload_folder": folder_mapping[upload_folder],
            "faces": len(face_data),
            "size": size,
            "url": url
        }
        response = supabase.table("image_data").insert(image_data).execute()
        if not response.data:
            print("Failed to insert image data")
            return
        
        # Retrieve the inserted image ID
        image_id = response.data[0]["id"]

        # Prepare face data for batch insert
        face_records = [
            {
                "image_id": image_id,
                "face_url": face_url,
                "age": age,
                "age_range": age_range,
                "gender": gender,
                "ethnicity": ethnicity,
                "emotion": emotion
            }
            for face_url, age, age_range, gender, ethnicity, emotion in face_data
        ]
        
        # Insert face data into the 'face_data' table
        face_response = supabase.table("face_data").insert(face_records).execute()
        if not face_response.data:
            print("Failed to insert face data")
        else:
            print("Data successfully inserted")
    except Exception as e:
        print(f"An error occurred while inserting data into Supabase: {e}")

def upload_data_to_cloud(server_data, folder):
    try:
        image = server_data["original_image"]
        faces = server_data["faces"]
        size = len(image)

        if len(faces) == 0:
            print("No faces detected.")
            return 
        face_folder = f"{folder}/Face Images"
        image_url = cloudinary.uploader.upload(image, folder=folder)["url"]
        face_data = []
        for face in faces:
            face_image = face["image"]
            face_url = cloudinary.uploader.upload(face_image, folder=face_folder)["url"]
            face_data.append((face_url, face["age"], face["age_range"], face["gender"], face["ethnicity"], face["emotion"]))  
        
        insert_user_data(folder, image_url, size, face_data)

    except Exception as e:
        print(f"An error occurred while uploading the image: {e}")
    
def upload_video_to_cloud(path):
    folder = "UploadedVideo" 
    video_url = cloudinary.uploader.upload(path, folder=folder, resource_type="video")["secure_url"]
    return video_url


def add_request(name, email):
    exist_username = supabase.table("request_users").select("username").execute().data
    password = create_password(length=16)  
    encrypted_password = encrypt_password(password, encryption_key)
    data = {
        "name": name,
        "mail": email,
        "username": create_username(email, exist_username),
        "password": encrypted_password, 
        "status": "Pending"
    }
    supabase.table('request_users').insert(data).execute()
    
def get_data_from_cloud():
    try:
        image_response = supabase.table("image_data").select("*").execute()
        face_response = supabase.table("face_data").select("*").execute()
        image_data, face_data = image_response.data, face_response.data
        return format_data(image_data, face_data)
    except Exception as e:
        print(f"An error occurred while fetching data from Supabase: {e}")
        return None
    
def get_user_requests():
    try:
        request_user_response = supabase.table("request_users").select("*").execute()
        return request_user_response.data
    except Exception as e:
        print(f"An error occurred while fetching data from Supabase: {e}")
        return None  
      
def update_request(id, action):
    if action == "approve":
        response = supabase.table('request_users').select('username', 'password').eq('id', id).execute()
        data = response.data
        username = data[0]['username']
        password = decrypt_password(data[0]['password'], encryption_key)
        print(username, password)
        supabase.table("request_users").update({"status": "Approved"}).eq("id", id).execute()
    else:
        supabase.table("request_users").delete().eq("id", id).execute()

def is_super_user(name, my_password):
    response = supabase.table('request_users').select('*').eq('username', name).execute()
    data = response.data
    if not data:  # Check if user data exists
        return False
    
    password = decrypt_password(data[0]['password'], encryption_key)
    status = data[0]['status']
    
    if password == my_password and status == 'Approved':
        return True
    else:
        return False


