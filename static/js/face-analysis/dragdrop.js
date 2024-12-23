document.addEventListener('DOMContentLoaded', () => {
    const uploadBox = document.getElementById('upload-box');
    const fileInput = document.getElementById('file-input');
    const uploadContainer = document.getElementById('upload-container');

    // Add drag event listeners
    uploadContainer.addEventListener('dragover', (event) => {
        event.preventDefault();
        uploadBox.classList.add('drag-over'); 
    });

    uploadContainer.addEventListener('dragleave', () => {
        uploadBox.classList.remove('drag-over');
    });

    uploadContainer.addEventListener('drop', (event) => {
        handleDrop(event);
    });

    fileInput.addEventListener('change', () => {
        handleFiles(fileInput.files);
    });

    // Function to handle drop event
    function handleDrop(event) {
        event.preventDefault();
        uploadBox.classList.remove('drag-over');
        const files = event.dataTransfer.files;
        handleFiles(files);
    }

    // Placeholder function to handle files (modify as needed)
    function handleFiles(files) {
        if (files.length > 0) {
            fileInput.files = files;
            var button = document.getElementById('select-file-button');
            var fileName = files.length > 0 ? files[0].name : 'Select File';
            button.textContent = fileName;        
        }
    }
});
