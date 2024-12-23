const webcamContainerElement = document.getElementById('webcam-container');
const webcamElement = document.getElementById('webcam');
const webcamClickElement = document.getElementById('webcam-click');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('capture-button');
const loadingIndicator = document.getElementById('loading-indicator');

const displayWidth = "100%";  // Set the desired display width
const displayHeight = '100%'; // Set the desired display height

let stream; // Variable to store the webcam stream

// Access webcam (do not limit the resolution to get the highest quality available)
navigator.mediaDevices.getUserMedia({
  video: { 
    width: { ideal: 1280 },  // Set ideal width for HD
    height: { ideal: 720 }   // Set ideal height for HD
  }
}).then(mediaStream => {
    stream = mediaStream; // Store the stream
    webcamElement.srcObject = stream;
    webcamElement.onloadedmetadata = () => {
      // Set the display dimensions for the video element using CSS (not the actual stream resolution)
      webcamElement.style.width = `${displayWidth}`;
      webcamElement.style.height = `${displayHeight}`;
      webcamElement.play();
    };
  })
  .catch(err => {
    console.error('Webcam access error:', err);
  });

// Capture snapshot when button is clicked
captureButton.addEventListener('click', () => {
  captureButton.style.display = 'none';
  loadingIndicator.style.display = 'block';
  const context = canvas.getContext('2d');
  if (context) {
    // Wait until the webcam video is loaded
    if (webcamElement.videoWidth && webcamElement.videoHeight) {
      // Set canvas dimensions to match the original (highest quality) webcam video
      canvas.width = webcamElement.videoWidth;
      canvas.height = webcamElement.videoHeight;
      
      // Draw the video frame to the canvas (this will be at the highest quality)
      context.drawImage(webcamElement, 0, 0, canvas.width, canvas.height);

      // Get image data as base64
      const imageData = canvas.toDataURL('image/jpeg');
      stream.getTracks().forEach(track => track.stop());

      // Hide the video element and show the canvas
      webcamElement.style.display = 'none';
      webcamClickElement.src = imageData;
      webcamClickElement.style.display = 'block';
      
      // Send image to server
      fetch('/upload_snapshot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: imageData })
      })
        .then(response => response.json())
        .then(data => {
          (data.body.length == 0)?emptyCarousel():populateCarousel(data.body);
          document.getElementById("webcam-box").style.display = "none";
          document.getElementById("results").style.display = "";
        })
        .catch(error => {
          console.error('Error uploading snapshot:', error);
        });
    } else {
      console.error('Webcam video dimensions are not available');
    }
  } else {
    console.error('Failed to get canvas context');
  }
});
