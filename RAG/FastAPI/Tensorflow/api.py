from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import joblib
import samples.tensorflow as tf
import uvicorn

EXPECTED_COLS = ["sqft", "bedrooms", "bathrooms", "age", "floors", "garage", "lot_size", "city_index"]

class HouseInput(BaseModel):
    sqft: float
    bedrooms: float
    bathrooms: float
    age: float
    floors: float
    garage: float
    lot_size: float
    city_index: float

app = FastAPI(title="House Price Predictor (TensorFlow)")

# ---- load artifacts ----
x_scaler = joblib.load("x_scaler.pkl")
y_scaler = joblib.load("y_scaler.pkl")
model = tf.keras.models.load_model("model.keras")

# (optional) sanity check
in_features = model.input_shape[-1] if hasattr(model, "input_shape") else len(EXPECTED_COLS)
if in_features is not None and in_features != len(EXPECTED_COLS):
    raise RuntimeError(f"Model expects {in_features} features but API is configured for {len(EXPECTED_COLS)}")

@app.get("/health")
def health():
    return {
        "status": "ok",
        "expected_columns": EXPECTED_COLS,
        "in_features": int(in_features) if in_features is not None else None,
    }

@app.post("/predict")
def predict(body: HouseInput):
    row = [
        body.sqft,
        body.bedrooms,
        body.bathrooms,
        body.age,
        body.floors,
        body.garage,
        body.lot_size,
        body.city_index,
    ]
    X = np.asarray([row], dtype=np.float32)
    Xs = x_scaler.transform(X).astype(np.float32)

    # TF returns numpy by default
    y_scaled = model.predict(Xs, verbose=0)          # shape (1,1)
    y = y_scaler.inverse_transform(y_scaled)         # back to original units

    return {"predicted_price": float(y[0, 0])}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
