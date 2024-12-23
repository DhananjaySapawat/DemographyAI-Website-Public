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


// Upload the selected file to the server
document.getElementById('server-upload').addEventListener('click', function() {
    var fileInput = document.getElementById('file-input');
    const errorMessage = document.getElementById('error-message');
    const file = fileInput.files.length > 0 ? fileInput.files[0] : null;
    const supportedFormats = ["jpg", "jpeg", "png", "webp"];

    if (!file) {
        errorMessage.textContent = "No file selected. Please choose a file to upload.";
        errorMessage.style.display = "block";
        return;
    }
    const fileExtension = file.name.split(".").pop().toLowerCase();
    if (!supportedFormats.includes(fileExtension)) {
        errorMessage.textContent = "Invalid file format. Please upload a file in JPG, JPEG, PNG, or WEBP format.";
        errorMessage.style.display = "block";
        return;
    }
    
    let formData = new FormData();
    formData.append('file', file);

    document.getElementById("server-upload").textContent  = 'Loading...';
    document.getElementById("server-upload").disabled = true;
    errorMessage.style.display = "None";
        
    // Send image to server
    fetch('/upload_file', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {        
        (data.body.length == 0)?emptyCarousel():populateCarousel(data.body);
        document.getElementById("upload-container").style.display = "none";
        document.getElementById("results").style.display = "";
    })
    .catch(error => {
        console.error('Error uploading Image:', error);
    });

});
