from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from helper.image_helpers import extract_face_data, convert_canvas_to_cv, process_uploaded_image
from helper.video_helpers import process_upload_video
from helper.cloud_functions import get_data_from_cloud, upload_data_to_cloud, add_request, get_user_requests, update_request, is_super_user
from helper.cloud_helper import get_filter_data, get_encrpt_user_requests
from dotenv import load_dotenv
import os
from datetime import timedelta
import time
from threading import Thread

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
encryption_key = os.getenv("ENCRYPTION_KEY")

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.permanent_session_lifetime = timedelta(hours=1)

progress = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload')
def upload():
    return render_template('face-analysis/upload.html')

@app.route('/upload_file', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    image_data = process_uploaded_image(uploaded_file)
    user_data, server_data = extract_face_data(image_data)
    upload_data_to_cloud(server_data, "Uploaded Images")
    return user_data

@app.route('/upload_video')
def upload_video():
    return render_template('face-analysis/upload_video.html')
def start_video_processing(uploaded_file, video_id):
    file_content = uploaded_file.read()  
    url = process_upload_video(file_content, progress[video_id])
    progress[video_id]["url"] = url 
    return 

@app.route('/upload_video_file', methods=['POST'])
def upload_video_file():
    uploaded_file = request.files['file']
    global progress
    video_id = len(progress)
    progress[video_id] = {"percent": 0, "url" : None}
    Thread(target=start_video_processing, args=(uploaded_file, video_id)).start()
    return jsonify({"video_id": video_id})

@app.route('/upload_video_progress/<video_id>', methods=['GET'])
def get_progress(video_id):
    global progress
    return jsonify(progress[int(video_id)])

@app.route('/snapshot')
def snapshot():
    return render_template('face-analysis/snapshot.html')

@app.route('/upload_snapshot', methods=['POST'])
def upload_snapshot():
    data = request.get_json()
    image_data = convert_canvas_to_cv(data['image'])
    user_data, server_data = extract_face_data(image_data, is_webcam=True)
    upload_data_to_cloud(server_data, "Snapshot Images")
    return user_data

@app.route('/webcam')
def webcam():
    feature = request.args.get('feature')
    return render_template('face-analysis/webcam.html', feature=feature)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['username'] = username
            session.permanent = True 
            session['login_time'] = time.time()  
            session['user_type'] = 'admin'  
            return redirect(url_for('dashboard'))
        
        elif is_super_user(username, password):
            session['username'] = username
            session.permanent = True 
            session['login_time'] = time.time()  
            session['user_type'] = 'super_user'  
            return redirect(url_for('dashboard'))
        
        else:
            flash('Invalid credentials. Please try again', 'error')
            return redirect(url_for('admin_login'))
    
    return render_template('admin/login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  
    return render_template('admin/login.html')

@app.route('/admin_access')
def admin_access():
    return render_template('admin/admin_access.html')

@app.route('/admin-request', methods=['POST'])
def admin_request():
    name = request.form.get('name')
    email = request.form.get('email')
    if not name or not email or name.strip(' ') == '':
        flash("Please fill out all fields!", "error")
        return redirect(url_for('admin_access'))
    flash("Your request has been submitted successfully!", "success")
    add_request(name, email)
    return redirect(url_for('admin_access'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('admin_login'))
    
    current_time = time.time()
    session_lifetime = current_time - session['login_time']
    
    if session_lifetime > 3600:  
        session.pop('username', None)  
        flash('Your session has expired. Please log in again.', 'error')
        return redirect(url_for('admin_login'))

    folder = request.args.get('folder')
    date_size = request.args.get('date_size')
    data = get_data_from_cloud()
    filter_data = get_filter_data(data, folder, date_size)
    return render_template('admin/dashboard.html', data=filter_data)

@app.route('/access_requests')
def access_requests():
    if 'username' not in session:
        return redirect(url_for('admin_login'))
    
    current_time = time.time()
    session_lifetime = current_time - session['login_time']
    
    if session_lifetime > 3600:  
        session.pop('username', None)
        flash('Your session has expired. Please log in again.', 'error')
        return redirect(url_for('admin_login'))
    
    if session.get('user_type') != 'admin':
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('admin_login')) 

    user_requests = get_user_requests()
    encrypted_user_requests = get_encrpt_user_requests(user_requests, encryption_key)
    return render_template('admin/access_requests.html', users=encrypted_user_requests)

@app.route('/process_request/<int:user_id>/<action>')
def process_request(user_id, action):
    update_request(int(user_id), action)
    return redirect(url_for('access_requests'))

@app.route('/contact')
def contact():
    email = os.getenv("GMAIL")
    instagram = os.getenv("INSTAGRAM")
    facebook = os.getenv("FACEBOOK")
    linkedin = os.getenv("LINKEDIN")
    github = os.getenv("GITHUB")
    return render_template('info/contact.html', email=email, instagram=instagram, facebook=facebook, linkedin=linkedin, github=github)

@app.route('/privacy')
def privacy():
    email = os.getenv("GMAIL")
    date = "4 December 2024"
    return render_template('info/privacy.html', email=email, date=date)

@app.route('/about')
def about():
    return render_template('info/about.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':  
   app.run()