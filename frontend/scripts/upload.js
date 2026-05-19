const API_URL = 'https://8000-01kr0y1n182efpkptj5kbabp8j.cloudspaces.litng.ai/api/predict';

// DOM elements
const uploadBox   = document.getElementById('upload-box');
const fileInput   = document.getElementById('fileInput');
const fileName    = document.getElementById('fileName');
const resultsCard = document.getElementById('results-card');
const resultsBody = document.getElementById('results-body');
const errorMsg    = document.getElementById('upload-error');
const loadingSpinner = document.getElementById('upload-loading');

// Click upload box --> trigger file input
uploadBox.addEventListener('click', () => fileInput.click());

// Drag and drop
uploadBox.addEventListener('dragover', e => {
  e.preventDefault();
  uploadBox.classList.add('border-primary');
});

uploadBox.addEventListener('dragleave', () => {
  uploadBox.classList.remove('border-primary');
});

uploadBox.addEventListener('drop', e => {
  e.preventDefault();
  uploadBox.classList.remove('border-primary');
  const file = e.dataTransfer.files[0];
  if (file) handleFile(file);
});

// File input change
fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  if (file) handleFile(file);
});

// Main handler
async function handleFile(file) {
  // Validate CSV
  if (!file.name.endsWith('.csv')) {
    showError('Only CSV files are accepted.');
    return;
  }

  // Update UI
  fileName.textContent  = file.name;
  hideError();
  showLoading(true);
  resultsCard.style.display = 'none';

  // Build form data
  const formData = new FormData();
  formData.append('file', file);

  // Get selected model (lowercase for backend)
  const model = (window.getModel ? window.getModel() : 'lstm').toLowerCase();
  const url   = `${API_URL}?model=${model}`;

  try {
    const response = await fetch(url, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const err = await response.json();
      showError(err.detail || `Server error: ${response.status}`);
      return;
    }

    const data = await response.json();
    renderResults(data.predictions);

  } catch (err) {
    showError('Could not reach the server. Make sure the backend is running.');
  } finally {
    showLoading(false);
  }
}

// Render results table
function renderResults(predictions) {
  if (!predictions || predictions.length === 0) {
    showError('No predictions returned. CSV may be too short (needs at least 128 rows).');
    return;
  }

  resultsBody.innerHTML = '';

  predictions.forEach(p => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${p.window}</td>
      <td>${formatTime(p.start)} – ${formatTime(p.end)}</td>
      <td><span class="badge ${activityBadgeClass(p.predicted_activity)}">${p.predicted_activity}</span></td>
      <td>${p.confidence.toFixed(1)}%</td>
    `;
    resultsBody.appendChild(row);
  });

  resultsCard.style.display = 'block';
}

// Helpers
function formatTime(ms) {
  // Convert milliseconds to mm:ss.SSS
  const totalSeconds = ms / 1000;
  const minutes = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
  const seconds = (totalSeconds % 60).toFixed(2).padStart(5, '0');
  return `${minutes}:${seconds}`;
}

function activityBadgeClass(activity) {
  const map = {
    'Walking':            'text-bg-success',
    'Walking Upstairs':   'text-bg-primary',
    'Walking Downstairs': 'text-bg-info',
    'Sitting':            'text-bg-secondary',
    'Standing':           'text-bg-warning',
    'Laying':             'text-bg-danger',
  };
  return map[activity] || 'text-bg-secondary';
}

function showError(msg) {
  errorMsg.textContent = msg;
  errorMsg.style.display = 'block';
}

function hideError() {
  errorMsg.style.display = 'none';
}

function showLoading(show) {
  loadingSpinner.style.display = show ? 'block' : 'none';
}
