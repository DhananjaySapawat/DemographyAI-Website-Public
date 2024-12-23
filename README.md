# DemographyAI

DemographyAI is a web application designed for face detection and analysis. The app allows users to upload images and videos or take snapshots using a webcam, and it returns the following features for all detected faces:

- **Age** (e.g., age ranges: 0-9, 10-19, etc.)
- **Gender** (Female or Male)
- **Ethnicity** (Asian, Black, Indian, Others, White)
- **Emotion** (Anger, Contempt, Disgust, Fear, Happy, Neutral, Sad, Surprise)

## Live Preview URL
You can access the live version of the application here: [DemographyAI](https://demography-ai.onrender.com/)

## Key Features

### Upload Options:
- Users can upload images and videos.
- Snapshots can be taken directly using a webcam.
- Live webcam detection

### Feature Detection:
- Detects and returns **age**, **gender**, **ethnicity**, and **emotion** for all faces in an image or video.

### Dashboard:
- Displays all uploaded images and videos.
- Ensures privacy by restricting access to users with admin privileges.

## Technology Stack:
- **Frontend**: Custom-built interface (without Bootstrap).
- **Backend**: Flask and PyTorch.
- **Database**: Supabase.
- **Cloud Storage**: Cloudinary for storing uploaded images and videos.
- **Hosting**: Deployed on AWS.

## Requirements
- Python 3.9.0

## Directory Structure
- `app.py`: Main application file.
- `helper/`: Contains utility modules for processing images, videos, cloud operations, and models.
  - `image_helpers.py`: Functions for processing images and extracting face data.
  - `video_helpers.py`: Functions for processing video uploads.
  - `models.py`: Model integration for face analysis.
  - `cloud_functions.py`: Cloudinary and Supabase integration.
  - `cloud_helper.py`: Helper functions for encryption and data formatting.
- `templates/`: HTML templates for rendering web pages.
- `static/`: Static assets like CSS, JavaScript, and images.

## Key Endpoints

| **Endpoint**               | **Description**                                    |
|----------------------------|----------------------------------------------------|
| `/`                        | Home page.                                         |
| `/upload`                  | Upload face images.                                |
| `/upload_file`             | Process uploaded image.                            |
| `/upload_video`            | Upload videos for analysis.                        |
| `/upload_video_file`       | Process uploaded video.                            |
| `/upload_video_progress`   | Check progress of video processing.                |
| `/snapshot`                | Capture and analyze snapshots.                     |
| `/admin_login`             | Admin login page.                                  |
| `/dashboard`               | Admin dashboard.                                   |
| `/access_requests`         | View user access requests (Admin only).            |
| `/process_request`         | Approve or reject user requests (Admin only).      |
| `/contact`                 | Contact information page.                          |
| `/about`                   | About the project.                                 |

## Model Repository
All the models developed for DemographyAI are available at the following GitHub repository: [DemographyAI Models](https://github.com/DhananjaySapawat/DemographyAI_Models.git)

## How to Run the Project
### Clone the Repository:
```bash
git clone https://github.com/DhananjaySapawat/DemographyAI-Website.git
cd DemographyAI-Website
```

### Create a Virtual Environment:
For **Windows**:
```bash
python -m venv venv
```

For **macOS/Linux**:
```bash
python3 -m venv venv
```

### Activate the Virtual Environment:
For **Windows**:
```bash
.\venv\Scripts\activate
```

For **macOS/Linux**:
```bash
source venv/bin/activate
```

### Install Dependencies:
```bash
pip install -r requirements.txt
```


### Configure Environment Variables:
Create a `.env` file in the project root and add your credentials:

#### Flask Configuration:
- `SECRET_KEY=<your_secret_key>`
- `ADMIN_USERNAME=<admin_username>`
- `ADMIN_PASSWORD=<admin_password>`

#### Cloudinary:
- `CLOUD_NAME=<cloudinary_cloud_name>`
- `API_KEY=<cloudinary_api_key>`
- `API_SECRET=<cloudinary_api_secret>`

#### Supabase:
- `SUPABASE_URL=<supabase_url>`
- `SUPABASE_KEY=<supabase_key>`

#### Social Links (for Contact Page):
- `GMAIL=<your_email>`
- `INSTAGRAM=<instagram_link>`
- `FACEBOOK=<facebook_link>`
- `LINKEDIN=<linkedin_link>`
- `GITHUB=<github_link>`

#### Encryption Key:
- `ENCRYPTION_KEY=<encryption_key>`

### Run the Application:
```bash
python app.py
```

### Access the App:
Open [http://localhost:5000](http://localhost:5000) in your web browser.

## Admin Access
- Only users with admin access can view the dashboard to ensure privacy.
- Admins can view all uploaded images and videos.

## License
This project is licensed under the MIT License.
