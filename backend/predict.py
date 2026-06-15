import numpy as np
import pandas as pd
from pathlib import Path
from tensorflow import keras
from preprocess import preprocess_data

classes = [
    'Walking',
    'Walking Upstairs',
    'Walking Downstairs',
    'Sitting',
    'Standing',
    'Laying'
]

models = {
    'cnn': 'cnn.h5',
    'lstm': 'lstm.h5',
    'gru': 'gru.h5',
    'rnn': 'rnn.h5'
}

MODEL_DIR = Path(__file__).parent.parent / 'models'
model_cache = {}

def load_model(model_name):
    if model_name not in model_cache:
        model_path = MODEL_DIR / models[model_name]
        model_cache[model_name] = keras.models.load_model(model_path)
    return model_cache[model_name]

def predict(df, model_name):
    model = load_model(model_name)

    # Preprocess the data
    windows, time = preprocess_data(df)

    # Make predictions
    predictions = model.predict(windows)
    results = []
    for i, pred in enumerate(predictions):
        predicted_label = classes[np.argmax(pred)]
        results.append({
            'window':             int(time[i]['window']),
            'start':              float(time[i]['t_start_ms']),
            'end':                float(time[i]['t_end_ms']),
            'predicted_activity': predicted_label,
            'all_probabilities':  {classes[j]: float(pred[j]) for j in range(len(classes))},
            'confidence':         float(np.max(pred)) * 100
        })

    return results
