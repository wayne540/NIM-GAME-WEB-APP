# backend/server.py
import os
import uuid
import pickle
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from nim import Nim, NimAI, train

# Initialize Flask app
app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")
CORS(app)

# Store games in memory
GAMES = {}

# Make sure AI file path is consistent with play.py
AI_FILE = os.path.join("backend", "nim_ai.pkl")

# Load AI if exists, otherwise create a fresh one
if os.path.exists(AI_FILE):
    with open(AI_FILE, "rb") as f:
        AI = pickle.load(f)
    print(f"✅ Loaded pre-trained AI from {AI_FILE}")
else:
    AI = NimAI()
    print("⚡ No pre-trained AI found, using fresh AI")

# -----------------------------
# Routes
# -----------------------------

@app.route("/api/new-game", methods=["POST"])
def new_game():
    """Start a new Nim game."""
    data = request.get_json(force=True)
    player = data.get("player", 0)  # 0 = human, 1 = AI goes first

    game_id = str(uuid.uuid4())
    game = Nim()
    GAMES[game_id] = {
        "game": game,
        "player": player,  # whose turn it is
        "winner": None
    }

    return jsonify({"game_id": game_id, "state": game.piles, "player": player})


@app.route("/api/state/<game_id>")
def get_state(game_id):
    """Return the state of a given game."""
    game_data = GAMES.get(game_id)
    if not game_data:
        return jsonify({"error": "Game not found"}), 404

    return jsonify({
        "state": game_data["game"].piles,
        "player": game_data["player"],
        "winner": game_data["winner"]
    })


@app.route("/api/move/<game_id>", methods=["POST"])
def make_move(game_id):
    """Apply a move for the human player."""
    game_data = GAMES.get(game_id)
    if not game_data:
        return jsonify({"error": "Game not found"}), 404

    move = request.get_json(force=True).get("move")
    game = game_data["game"]

    try:
        game.move(move)
    except Exception:
        return jsonify({"error": "Invalid move"}), 400

    # Check for winner
    if game.winner is not None:
        # The previous player actually won, since turn already switched
        game_data["winner"] = 0 if game_data["player"] == 1 else 1

    # Switch turns
    game_data["player"] = 1 if game_data["player"] == 0 else 0

    return jsonify({
        "state": game.piles,
        "player": game_data["player"],
        "winner": game_data["winner"]
    })


@app.route("/api/ai-move/<game_id>", methods=["POST"])
def ai_move(game_id):
    """Let the AI make a move."""
    game_data = GAMES.get(game_id)
    if not game_data:
        return jsonify({"error": "Game not found"}), 404

    game = game_data["game"]
    move = AI.choose_action(game.piles, epsilon=False)
    game.move(move)

    # Check for winner
    if game.winner is not None:
        game_data["winner"] = 0 if game_data["player"] == 1 else 1

    # Switch turns
    game_data["player"] = 1 if game_data["player"] == 0 else 0

    return jsonify({
        "move": move,
        "state": game.piles,
        "player": game_data["player"],
        "winner": game_data["winner"]
    })


@app.route("/api/train", methods=["POST"])
def train_ai():
    """Retrain the AI and save it."""
    global AI
    AI = train(10000)
    with open(AI_FILE, "wb") as f:
        pickle.dump(AI, f)
    return jsonify({"status": f"AI trained and saved at {AI_FILE}"})


# -----------------------------
# Frontend (React build serving)
# -----------------------------

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    """Serve React frontend."""
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
