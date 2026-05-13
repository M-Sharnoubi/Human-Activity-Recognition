# Human Activity Recognition (HAR) — All Phases

A full machine learning pipeline for classifying human physical activities from smartphone sensor data, organized across three progressive phases from classical ML to advanced deep learning.

---

## Dataset

**UCI HAR Dataset** — sensor readings from a Samsung Galaxy S II worn on the waist by 30 subjects performing 6 activities.

| Split | Samples | Features |
|-------|---------|----------|
| Train | 7,352   | 561      |
| Test  | 2,947   | 561      |

**Activities:** Walking, Walking Upstairs, Walking Downstairs, Sitting, Standing, Laying

**Sensors:** Body accelerometer (X/Y/Z), Gyroscope (X/Y/Z), Gravity accelerometer (X/Y/Z), plus magnitude and jerk features.

**Input files expected at:** `/content/train.csv` and `/content/test.csv`

---

## Project Structure

```
All_Phases.ipynb
├── Imports & Setup
├── Phase 1 — Data & Classical Machine Learning
│   ├── 1.1 Exploratory Data Analysis
│   ├── 1.2 Dimensionality Reduction (PCA & LDA)
│   ├── 1.3 KNN & Naïve Bayes
│   └── 1.4 Ensemble Methods (Random Forest & Gradient Boosting)
├── Phase 2 — Deep Learning
│   ├── 2.1 1D-CNN for Sensor Classification
│   ├── 2.2 Optimizer Comparison (Adam vs SGD)
│   ├── 2.3 Autoencoder — Anomaly Detection
│   └── 2.4 Transfer Learning (Subject-to-Subject)
├── Phase 3 — Advanced Sequence Models
│   ├── 3.1 RNN
│   ├── 3.2 GRU
│   ├── 3.3 LSTM
│   └── 3.4 Transformer (BERT-style fine-tuning)
└── Full Model Comparison — All Phases
```

---

## Phase 1 — Classical Machine Learning

### EDA Highlights
- 561 features; **no missing values, no duplicate rows**
- 12 representative features selected (one per sensor/axis) for visualization
- FFT frequency-domain analysis at 50 Hz sampling rate
- Outlier analysis using IQR per activity (static activities have more outliers than dynamic ones due to their narrow signal range)

### Dimensionality Reduction
| Method | Detail |
|--------|--------|
| PCA | Scree plot + cumulative variance; `n_95` components retain 95% variance |
| LDA | Maximizes class separability; 2D scatter shows strong activity clustering |

### Classifiers
| Model | Notes |
|-------|-------|
| KNN (k=5, Euclidean) | Trained on PCA-reduced features |
| Gaussian Naïve Bayes | Trained on PCA-reduced features |

Both include **ROC curves** (per-class + macro-AUC) and confusion matrices.

### Ensemble Methods
- **Random Forest** — tuned with `RandomizedSearchCV` (3-fold stratified, 25 iterations)
- **Gradient Boosting** — tuned with `HalvingRandomSearchCV` (aggressive elimination)
- **Cross-subject evaluation** using `StratifiedGroupKFold` (3 folds, grouped by subject)
- Feature importance plot (top 20 features from Random Forest)

---

## Phase 2 — Deep Learning

### 1D-CNN Architecture
Three convolutional blocks (64 → 128 → 256 filters, kernel=3), each followed by BatchNorm + ReLU + MaxPool + Dropout(0.2), then a Dense(128) + Dropout(0.5) + Softmax head. Input shape: `(561, 1)`.

### Optimizer Comparison
Same CNN architecture trained with:
- **Adam** (lr=1e-3)
- **SGD + Momentum** (lr=0.01, momentum=0.9)

Side-by-side validation accuracy/loss curves + test metrics table.

### Autoencoder — Anomaly Detection
Symmetric encoder-decoder on 561-dim flat features (bottleneck: 32 units). Anomalies are samples whose **reconstruction MSE exceeds mean + 2σ** of the test set error. Results shown per activity.

### Transfer Learning
Pre-trains the CNN on all subjects except subject 26, then fine-tunes on 50 samples from subject 26. Variants compared:
- Pretrained (no fine-tune)
- Fine-tuned with Adam (lr=1e-4)
- Fine-tuned with SGD (lr=1e-4)
- Baseline trained from scratch

> Note: features are reshaped to `(63, 9)` (padded from 561 → 567) for the transfer learning experiment.

---

## Phase 3 — Advanced Sequence Models

All recurrent models reshape the 561 features into a sequence of shape `(1, 561)` (single timestep).

### RNN
SimpleRNN(32) with L2 regularization (λ=0.005) + Dropout(0.5) + Dense head.

### GRU
Two GRU layers (128 → 64 units) with recurrent dropout + BatchNorm + Dropout, followed by Dense(64) + Softmax. Full evaluation: training curves, confusion matrix, per-class ROC, per-class F1 bar chart.

### LSTM
*(Architecture defined in notebook.)*

### Transformer (BERT-style)
Custom transformer built from scratch on sensor data:
- Input projected to `embed_dim=32`
- Positional embeddings (learned)
- 2 Transformer encoder blocks (4 attention heads, FFN dim=64)
- Global Average Pooling → Dense(128) → Softmax

Full evaluation mirrors the GRU section (curves, CM, ROC, per-class F1).

---

## Final Comparison

All models are tracked in a shared `all_results` list and rendered as a sorted horizontal bar chart (Accuracy + Macro F1) covering all three phases.

---

## Dependencies

```
numpy, pandas, matplotlib, seaborn
scikit-learn
tensorflow / keras
```

Install with:
```bash
pip install numpy pandas matplotlib seaborn scikit-learn tensorflow
```

---

## Helper Utilities

| Function | Purpose |
|----------|---------|
| `eval_keras(model, ...)` | Evaluates Keras model; appends to `all_results` |
| `eval_sklearn(model, ...)` | Evaluates sklearn model; appends to `all_results` |
| `plot_curves(history, title)` | Training/validation accuracy + loss curves |
| `plot_cm(y_true, y_pred, title)` | Confusion matrix display |

Early stopping is applied globally via `ES = EarlyStopping(patience=10, restore_best_weights=True)`.
