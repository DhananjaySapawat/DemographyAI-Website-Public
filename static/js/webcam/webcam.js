const videoElement = document.getElementById('webcam');
const canvas = document.getElementById('output');
const ctx = canvas.getContext('2d', { willReadFrequently: true });  

const feature = document.getElementById("feature-select").value;
const bg_color = 'rgb(35, 102, 11)';

async function setupCamera() {
    const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: false,
    });
    videoElement.srcObject = stream;
    return new Promise((resolve) => {
        videoElement.onloadedmetadata = () => {
            resolve(videoElement);
        };
    });
}

async function loadModel() {
    if (typeof blazeface === "undefined") {
        console.error("Blazeface is not loaded.");
        return null;
    }
    return await blazeface.load();
}

async function PredictionModel() {
    return await tf.loadGraphModel(model_path(feature));
}

async function detectFaces() {
    const model = await loadModel();
    const featurePredictionModel = await PredictionModel() 
    await setupCamera();
    videoElement.play();

    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;

    async function processFrame() {
        const predictions = await model.estimateFaces(videoElement, false);
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        if (predictions.length > 0) {
            predictions.forEach(async (face) => {
                const topLeft = face.topLeft;
                const bottomRight = face.bottomRight;

                const faceWidth = Math.floor(bottomRight[0] - topLeft[0]);
                const faceHeight = Math.floor(bottomRight[1] - topLeft[1]);
            
                let faceImage = tf.browser.fromPixels(videoElement)
                    .slice([Math.floor(topLeft[1]), Math.floor(topLeft[0]), 0], [faceHeight, faceWidth, 3])
                    .resizeNearestNeighbor([imageDimension, imageDimension]) 
                    .toFloat();

                const rectWidth = bottomRight[0] - topLeft[0];
                const rectHeight = bottomRight[1] - topLeft[1];

                const offsetY = bottomRight[1]; 

                ctx.beginPath();
                ctx.strokeStyle = bg_color;  
                ctx.lineWidth = 4;
                ctx.rect(topLeft[0], topLeft[1], rectWidth, rectHeight);  
                ctx.stroke();
                
                const fillRectHeight = 50; 
                ctx.fillStyle = bg_color;  
                ctx.fillRect(
                    topLeft[0],              
                    offsetY,              
                    rectWidth,               
                    fillRectHeight            
                );
                    
                const faceTensor = faceImage.div(tf.scalar(255.0)).transpose([2, 0, 1]).expandDims(0); 
                const featurePrediction = await featurePredictionModel.executeAsync(faceTensor); 
                const logit = featurePrediction.dataSync();
                const featureValue = find_value_by_logit(logit, feature); 
  
                ctx.fillStyle = "white";  
                ctx.font = "16px Arial";  
                ctx.strokeStyle = bg_color; 
                ctx.lineWidth = 4;

                ctx.fillText(
                    `${feature}: ${featureValue}`, 
                    topLeft[0] + 5,              
                    offsetY + 30,              
                );
                
                faceImage.dispose();
                faceTensor.dispose();
                featurePrediction.dispose();
                face.dispose();
            });
        }
        requestAnimationFrame(processFrame);
    }
    processFrame();
}

detectFaces();
