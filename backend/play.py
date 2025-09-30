# backend/play.py
from nim import train
import pickle
import os

# Ensure the model directory exists
MODEL_FILE = os.path.join("backend", "nim_ai.pkl")

print("⚙️ Training Nim AI... This may take a moment.")
ai = train(10000)  # Train the AI with 10,000 games

# Save the trained model
with open(MODEL_FILE, "wb") as f:
    pickle.dump(ai, f)

print(f"✅ Nim AI trained and saved at {MODEL_FILE}")
