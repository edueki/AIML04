from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import joblib
import torch
import torch.nn as nn
from typing import Optional
import uvicorn

# ----- Constants -----
EXPECTED_COLS = ["sqft", "bedrooms", "bathrooms", "age", "floors", "garage", "lot_size", "city_index"]

# ----- Model def (must match training arch) -----
class HousePricePredictor(nn.Module):
    def __init__(self, in_features: int):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(in_features, 16), nn.ReLU(),
            nn.Linear(16, 8),          nn.ReLU(),
            nn.Linear(8, 4),           nn.ReLU(),
            nn.Linear(4, 1),
        )
    def forward(self, x):
        return self.network(x)

# ----- Request schema: top-level JSON with named fields -----
class HouseInput(BaseModel):
    sqft: float
    bedrooms: float
    bathrooms: float
    age: float
    floors: float
    garage: float
    lot_size: float
    city_index: float

# ----- App & artifact load -----
app = FastAPI(title="House Price Predictor (PyTorch)")


x_scaler = joblib.load("x_scaler.pkl")
y_scaler = joblib.load("y_scaler.pkl")

# build model & load weights
device = torch.device("cpu")
model = HousePricePredictor(in_features=len(EXPECTED_COLS)).to(device)
state = torch.load("model.pth", map_location=device)  # saved via torch.save(model.state_dict(), ...)
model.load_state_dict(state)
model.eval()

@app.post("/predict")
def predict(body: HouseInput):
    # assemble row in the exact training order
    dataset = [
        body.sqft,
        body.bedrooms,
        body.bathrooms,
        body.age,
        body.floors,
        body.garage,
        body.lot_size,
        body.city_index,
    ]
    X = np.asarray([dataset], dtype=np.float32)

    # scale -> tensor -> predict -> inverse-scale
    Xs = x_scaler.transform(X).astype(np.float32)
    x_tensor = torch.as_tensor(Xs, dtype=torch.float32, device=device)
    with torch.no_grad():
        y_scaled = model(x_tensor)
    y = y_scaler.inverse_transform(y_scaled)                  # back to original price units

    return {"predicted_price": int(y[0, 0])}

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0", port=8000)