const carousel = document.getElementById('carousel');
const emptyResult = document.getElementById('emtpy-result');
const results = document.getElementById("results")
const carouselItems = document.getElementById('carousel-items');
const carouselPrev = document.getElementById('carousel-control-prev');
const carouselNext = document.getElementById('carousel-control-next');
var carouselCurrent;

var result_template = (src, age, gender, ethnicity, emotion, display) => {
  return ( `
        <div class="results-container" style="display: ${display};">
          <div id="cropped-image-container" class="cropped-image-container">
            <h3>Cropped Image</h3>
            <img id="cropped-image" src=${src} alt="Cropped Image" />
          </div>
      
          <div class="results-details">
            <div class="result-item">
              <h3>Age</h3>
              <p id="age">${age}</p>
            </div>
      
            <div class="result-item">
              <h3>Gender</h3>
              <p id="gender">${gender}</p>
            </div>
      
            <div class="result-item">
              <h3>Ethnicity</h3>
              <p id="ethnicity">${ethnicity}</p>
            </div>
      
            <div class="result-item">
              <h3>Emotion</h3>
              <p id="emotion">${emotion}</p>
            </div>
          </div>
        </div>
  `);
};

function populateCarousel(result_data) {
  carouselCurrent = 0;
  result_data.forEach((result, index) => {
    dynamic_html = result_template(
      'data:image/jpeg;base64,' + result.image,
      result.age,
      result.gender,
      result.ethnicity,
      result.emotion,
      (index == 0)?"flex":"none"
    );
    carouselItems.innerHTML += dynamic_html
  });
}

function emptyCarousel(){
  carousel.style.display = "none";
  emptyResult.style.display = "block";
  results.style.maxWidth = "350px";
  results.style.padding = "2rem";
  document.getElementById("results")
}
function prevResult(){
  var elements = document.getElementsByClassName("results-container");
  var current = carouselCurrent;
  carouselCurrent = (carouselCurrent - 1 + elements.length) % elements.length;
  elements[current].style.display = "none";
  elements[carouselCurrent].style.display = "flex";
}

function nextResult(){
  var elements = document.getElementsByClassName("results-container");
  var current = carouselCurrent;
  carouselCurrent = (carouselCurrent + 1) % elements.length;
  elements[current].style.display = "none";
  elements[carouselCurrent].style.display = "flex";
}

