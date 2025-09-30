# backend/play_and_save.py
from nim import train
import pickle, os

ai = train(10000)
with open("nim_ai.pkl", "wb") as f:
    pickle.dump(ai, f)
print("Saved nim_ai.pkl")
