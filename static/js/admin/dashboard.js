function openModal(item) {
    // Update modal with folder name, number of faces detected, and upload date
    document.getElementById('modal-detail-folder').textContent = `Folder: ${item.folder_name}`;
    document.getElementById('modal-detail-faces').textContent = `Face Detected: ${item.faces}`;
    document.getElementById('modal-detail-date').textContent = `Uploaded on : ${item.date}`;

    // Clear any existing content in the modal that displays face data
    const modal = document.getElementById('modal-face-data');
    modal.innerHTML = '';

    // Loop through each face data and populate the modal with face details
    item.face_data.forEach((face, index) => {
        // Create a container for each face's data
        const faceRow = document.createElement('div');
        faceRow.classList.add('face-row');

        // Add the face image to the face row
        const faceImage = document.createElement('img');
        faceImage.src = face.face_url;
        faceImage.alt = `Face ${index + 1}`;
        faceRow.appendChild(faceImage);

        // Create and populate a section for the face details (age, gender, etc.)
        const faceDetails = document.createElement('div');
        faceDetails.classList.add('face-details');
        faceDetails.innerHTML = `
            <p><strong>Face ${index + 1}</strong></p>
            <p><strong>Age:</strong> ${face.age}</p>
            <p><strong>Age Range:</strong> ${face.age_range}</p>
            <p><strong>Gender:</strong> ${face.gender}</p>
            <p><strong>Ethnicity:</strong> ${face.ethnicity}</p>
            <p><strong>Emotion:</strong> ${face.emotion}</p>
        `;

        // Append face details to the face row and the face row to the modal
        faceRow.appendChild(faceDetails);
        modal.appendChild(faceRow);
    });

    // Display the modal with the populated face data
    const imageModal = document.getElementById('imageModal');
    imageModal.style.display = 'block';

    // Scroll the modal body to the top for better visibility of new content
    const modal_body = document.getElementById("modal-body");
    modal_body.scrollTop = 0;
}

function closeModal() {
    // Hide the modal when the close button is clicked
    const imageModal = document.getElementById('imageModal');
    imageModal.style.display = 'none';
}
