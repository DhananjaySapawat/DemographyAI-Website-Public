const progressContainer = document.getElementById("progress-container");
const progressBar = document.getElementById("progress-bar");

// Function to update the button text to the selected file name
function updateButtonText() {
    var fileInput = document.getElementById('file-input');
    var button = document.getElementById('select-file-button');
    var fileName = fileInput.files.length > 0 ? fileInput.files[0].name : 'Select File';
    button.textContent = fileName;
}

// Change the button text on click to open the file input
document.getElementById('select-file-button').addEventListener('click', function() {
    document.getElementById('file-input').click();
});

// Add onchange event to the file input to trigger updateButtonText
document.getElementById('file-input').addEventListener('change', updateButtonText);

document.getElementById('server-upload').addEventListener('click', function() {
    var fileInput = document.getElementById('file-input');
    const errorMessage = document.getElementById('error-message');
    const file = fileInput.files.length > 0 ? fileInput.files[0] : null;
    const supportedFormats = ["mp4", "webm", "ogg"];
    const maxSizeInMB = 25; 
    const maxDurationInSeconds = 60; 

    // Check if a file is selected
    if (!file) {
        errorMessage.textContent = "No file selected. Please choose a file to upload.";
        errorMessage.style.display = "block";
        return;
    }

    const fileExtension = file.name.split(".").pop().toLowerCase();

    // Check for supported formats
    if (!supportedFormats.includes(fileExtension)) {
        errorMessage.textContent = "Invalid file format. Please upload a file in MP4, WebM, or OGG format.";
        errorMessage.style.display = "block";
        return;
    }

    // Check file size
    if (file.size > maxSizeInMB * 1024 * 1024) {
        errorMessage.textContent = `File size exceeds the maximum limit of ${maxSizeInMB} MB.`;
        errorMessage.style.display = "block";
        return;
    }

    // Check video duration
    const video = document.createElement("video");
    video.preload = 'metadata';
    video.src = URL.createObjectURL(file);
    video.onloadedmetadata = function() {
        if (video.duration > maxDurationInSeconds) {
            errorMessage.textContent = `Video duration exceeds the maximum limit of ${maxDurationInSeconds / 60} minutes.`;
            errorMessage.style.display = "block";
            return;
        }

        // Proceed with uploading after all checks pass
        let formData = new FormData();
        formData.append('file', file);

        // Hide upload button and show progress
        document.getElementById("server-upload").style.display  = 'none';
        errorMessage.style.display = "none";
        progressContainer.style.display = "";

        // Send video to server
        fetch('/upload_video_file', {
                method: 'POST',
                body: formData
        })
        .then(response => response.json())
        .then(data => {   
            updateProgress(data.video_id); 
        })
        .catch(error => {
            console.error('Error uploading Video:', error);
        });
    };
});


function updateProgress(video_id) {
    fetch(`/upload_video_progress/${video_id}`)
        .then(response => response.json())
        .then(data => {
            const progressBar = document.getElementById('progress-bar');
            progressBar.style.width = data.percent + "%";
            progressBar.textContent = data.percent + "%";

            if (data.url) {
                const videoElement = document.getElementById('processedVideo');
                videoElement.src = data.url;
                document.getElementById("upload-container").style.display = "none";
                document.getElementById("video-results").style.display = "";
            } else if (data.percent < 100) {
                setTimeout(() => updateProgress(video_id), 2000); 
            } else {
                progressBar.style.width = "100%";
                progressBar.textContent = "Almost Completed!!!";
                setTimeout(() => updateProgress(video_id), 1000);    
            }
        })
        .catch(error => console.error('Error fetching progress:', error));
}
