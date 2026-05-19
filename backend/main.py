from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from predict import predict as make_prediction
import pandas as pd
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

required_fields = [
    'body_acc_x', 'body_acc_y', 'body_acc_z',
    'body_gyro_x', 'body_gyro_y', 'body_gyro_z',
    'total_acc_x', 'total_acc_y', 'total_acc_z',
    'timestamp'
]

@app.post("/api/predict")
async def predict(file: UploadFile, model: str = 'cnn'):
    # Read the uploaded file
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))

    # Validate required fields
    missing_fields = [field for field in required_fields if field not in df.columns]
    if missing_fields:
        return {"error": f"Missing required fields: {', '.join(missing_fields)}"}

    # Make predictions using the specified model
    results = make_prediction(df, model_name=model)
    return {"predictions": results}