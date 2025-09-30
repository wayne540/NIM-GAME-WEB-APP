import os
import uuid
import pickle
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from nim import Nim, NimAI, train

app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")
CORS(app)

GAMES = {}
AI_FILE = os.path.join("backend", "nim_ai.pkl")

# Load or create AI
if os.path.exists(AI_FILE):
    with open(AI_FILE, "rb") as f:
        AI = pickle.load(f)
else:
    AI = NimAI()

# -----------------------------
# API Routes
# -----------------------------

@app.route("/api/new-game", methods=["POST"])
def new_game():
    data = request.get_json(force=True)
    initial = data.get("initial", [1,3,5,7])
    mode = data.get("mode", "normal")
    ai_player = data.get("ai_player", None)

    game_id = str(uuid.uuid4())
    game = Nim(initial)
    GAMES[game_id] = {
        "game": game,
        "player": 0,      # player 0 always starts
        "winner": None,
        "ai_player": ai_player
    }

    return jsonify({
        "game_id": game_id,
        "state": {
            "piles": game.piles,
            "player": 0,
            "winner": None,
            "mode": mode
        }
    })


@app.route("/api/state/<game_id>")
def get_state(game_id):
    game_data = GAMES.get(game_id)
    if not game_data:
        return jsonify({"error": "Game not found"}), 404

    game = game_data["game"]
    return jsonify({
        "state": {
            "piles": game.piles,
            "player": game_data["player"],
            "winner": game_data["winner"]
        }
    })


@app.route("/api/move/<game_id>", methods=["POST"])
def make_move(game_id):
    game_data = GAMES.get(game_id)
    if not game_data:
        return jsonify({"error": "Game not found"}), 404

    data = request.get_json(force=True)
    pile = data.get("pile")
    count = data.get("count")
    game = game_data["game"]

    try:
        game.move((pile, count))
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Check winner
    if game.winner is not None:
        game_data["winner"] = Nim.other_player(game_data["player"])

    # Switch turns
    game_data["player"] = Nim.other_player(game_data["player"])

    return jsonify({
        "state": {
            "piles": game.piles,
            "player": game_data["player"],
            "winner": game_data["winner"]
        }
    })


@app.route("/api/ai-move/<game_id>", methods=["POST"])
def ai_move(game_id):
    game_data = GAMES.get(game_id)
    if not game_data:
        return jsonify({"error": "Game not found"}), 404

    game = game_data["game"]
    move = AI.choose_action(game.piles, epsilon=False)
    game.move(move)

    # Check winner
    if game.winner is not None:
        game_data["winner"] = Nim.other_player(game_data["player"])

    # Switch turns
    game_data["player"] = Nim.other_player(game_data["player"])

    return jsonify({
        "move": move,
        "state": {
            "piles": game.piles,
            "player": game_data["player"],
            "winner": game_data["winner"]
        }
    })


@app.route("/api/train", methods=["POST"])
def train_ai():
    global AI
    AI = train(10000)
    with open(AI_FILE, "wb") as f:
        pickle.dump(AI, f)
    return jsonify({"status": "AI trained and saved"})


# -----------------------------
# Serve React
# -----------------------------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
