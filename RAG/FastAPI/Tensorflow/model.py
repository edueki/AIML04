# tensorflow==2.x
import pandas as pd
import numpy as np
import json
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import samples.tensorflow as tf
from samples.tensorflow import keras
from tensorflow.keras import layers

# 1) Load data
data = pd.read_csv("house_data.csv")
X = data.drop(columns=["price"])
Y = data[["price"]]

# 2) To numpy float32
X_new = X.to_numpy(dtype=np.float32)
Y_new = Y.to_numpy(dtype=np.float32)

# 3) Train/test split
x_train, x_test, y_train, y_test = train_test_split(
    X_new, Y_new, test_size=0.2, random_state=42
)

# 4) Scale features & target (same as your PyTorch code)
x_scaler = StandardScaler().fit(x_train)
y_scaler = StandardScaler().fit(y_train)

x_train_sc = x_scaler.transform(x_train).astype(np.float32)
x_test_sc  = x_scaler.transform(x_test).astype(np.float32)
y_train_sc = y_scaler.transform(y_train).astype(np.float32)
y_test_sc  = y_scaler.transform(y_test).astype(np.float32)

# 5) Build model (8 -> 16 -> 8 -> 4 -> 1)
model = keras.Sequential([
    layers.Dense(16, activation="relu", input_shape=(x_train_sc.shape[1],)),
    layers.Dense(8, activation="relu"),
    layers.Dense(4, activation="relu"),
    layers.Dense(1),
])

# 6) Compile: Adam(lr=0.001), MSE
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss="mse"
)

# Optional: print loss every 100 epochs to mimic your loop
class EveryHundred(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        if (epoch + 1) % 100 == 0:
            print(f"Epoch {epoch+1:4d}/1000 | loss: {logs['loss']:.6f}")

# 7) Train
model.fit(
    x_train_sc, y_train_sc,
    epochs=1000,
    batch_size=32,
    verbose=0,
    callbacks=[EveryHundred()]
)

# 8) (Optional) Evaluate on test (MSE in scaled space)
test_loss = model.evaluate(x_test_sc, y_test_sc, verbose=0)
print(f"Test MSE (scaled): {test_loss:.6f}")

# 9) Save artifacts
#    - Full TF model (architecture + weights)
model.save("model.keras")
#    - Or, if you prefer weights-only:
# model.save_weights("model.weights.h5")

#    - Scalers (same as your PyTorch code)
joblib.dump(x_scaler, "x_scaler.pkl")
joblib.dump(y_scaler, "y_scaler.pkl")

#    - Column order (so your API/Streamlit can map JSON correctly)
with open("columns.json", "w") as f:
    json.dump(list(X.columns), f)
