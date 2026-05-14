// Tab selection
const livePredictionTab = document.getElementById("live-prediction-tab");
const csvUploadTab = document.getElementById("csv-upload-tab");

const livePredictionContent = document.getElementById("live-sensor-prediction");
const csvUploadContent = document.getElementById("csv-upload");

function displayPredictionTab() {
  livePredictionTab.classList.add("active");
  csvUploadTab.classList.remove("active");
  livePredictionContent.style.display = "";
  csvUploadContent.style.display = "none";
}

function displayCSVTab() {
  csvUploadTab.classList.add("active");
  livePredictionTab.classList.remove("active");
  csvUploadContent.style.display = "";
  livePredictionContent.style.display = "none";
}

// Model selection
var selectedModel = "CNN";
window.getModel = () => selectedModel.toLowerCase();
var setModel = model => { selectedModel = model; };

document.querySelectorAll(".dropdown-item").forEach(item => {
item.addEventListener("click", e => {
  e.preventDefault();
  selectedModel = item.textContent.trim();
  document.querySelector(".nav-link.dropdown-toggle").textContent = selectedModel;
  setModel(selectedModel);
});
});