import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import joblib
import json
data = pd.read_csv("house_data.csv")
X = data.drop(columns=['price'])
Y = data[['price']]
X_new = X.to_numpy(dtype=np.float32)
Y_new = Y.to_numpy(dtype=np.float32)
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(X_new, Y_new, test_size=0.2, random_state=42)
from sklearn.preprocessing import StandardScaler
x_scalar = StandardScaler().fit(x_train)
y_scalar = StandardScaler().fit(y_train)
x_train_scalar = x_scalar.transform(x_train).astype(np.float32)
x_test_scalar = x_scalar.transform(x_test).astype(np.float32)
y_train_scalar = y_scalar.transform(y_train).astype(np.float32)
y_test_scalar = y_scalar.transform(y_test).astype(np.float32)
x_train_tensor = torch.from_numpy(x_train_scalar)
x_test_tensor = torch.from_numpy(x_test_scalar)
y_train_tensor = torch.from_numpy(y_train_scalar)
y_test_tensor= torch.from_numpy(y_test_scalar)
class HousePricePredictor(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(8,16),
            nn.ReLU(),
            nn.Linear(16,8),
            nn.ReLU(),
            nn.Linear(8,4),
            nn.ReLU(),
            nn.Linear(4,1)
        )
    def forward(self, x_train_data):
        return self.network(x_train_data)

model = HousePricePredictor() 
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
model.train()
epochs = 1000
for epoch in range(1, epochs+1):
    #1. Forward Pass
    y_predictions = model(x_train_tensor)
    #2. Calculate loss
    loss = criterion(y_predictions, y_train_tensor )
    #3. Optimize
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
torch.save(model.state_dict(), "model.pth")

joblib.dump(x_scalar, "x_scaler.pkl")   # feature scaler
joblib.dump(y_scalar, "y_scaler.pkl")   # target scaler

with open("columns.json", "w") as f:
    json.dump(X.columns.tolist(), f)