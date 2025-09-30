# backend/server.py
import os
import uuid
import pickle
from flask import Flask, jsonify, request, send_from_directory, abort
from flask_cors import CORS
from nim import Nim, NimAI, train  # your existing nim.py

APP_DIR = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(APP_DIR, "..", "frontend", "build")  # React build path
AI_PATH = os.path.join(APP_DIR, "nim_ai.pkl")

app = Flask(__name__, static_folder=BUILD_DIR, static_url_path="/")
CORS(app)

# In-memory store of active games: {game_id: {piles, player, winner, mode, ai_player}}
GAMES = {}

# Load or create AI
def load_ai():
    if os.path.exists(AI_PATH):
        try:
            with open(AI_PATH, "rb") as f:
                ai = pickle.load(f)
            print("Loaded trained AI from disk.")
            return ai
        except Exception as e:
            print("Failed to load AI:", e)
    print("No saved AI found. Using new untrained NimAI.")
    return NimAI()

AI = load_ai()


def serialize_game_state(game):
    return {
        "piles": game["piles"],
        "player": game["player"],
        "winner": game["winner"],
        "mode": game.get("mode", "normal")
    }


@app.route("/api/new-game", methods=["POST"])
def new_game():
    """
    Body JSON:
    {
      "initial": [1,3,5,7],
      "mode": "normal" | "misere",
      "ai_player": 0 or 1 or null
    }
    Response:
      { "game_id": str, "state": {...} }
    """
    data = request.get_json() or {}
    initial = data.get("initial", [1, 3, 5, 7])
    mode = data.get("mode", "normal")
    ai_player = data.get("ai_player", None)  # if set, AI will play that player

    # create game state dict (we keep plain data so JSON-friendly)
    game_id = str(uuid.uuid4())
    game = {
        "piles": initial.copy(),
        "player": 0,
        "winner": None,
        "mode": mode,
        "ai_player": ai_player
    }
    GAMES[game_id] = game
    return jsonify({"game_id": game_id, "state": serialize_game_state(game)}), 201


@app.route("/api/state/<game_id>", methods=["GET"])
def get_state(game_id):
    game = GAMES.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    return jsonify(serialize_game_state(game))


@app.route("/api/move/<game_id>", methods=["POST"])
def make_move(game_id):
    """
    Body JSON:
      { "pile": int, "count": int }
    """
    game = GAMES.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404

    if game["winner"] is not None:
        return jsonify({"error": "Game already finished", "state": serialize_game_state(game)}), 400

    data = request.get_json() or {}
    pile = data.get("pile")
    count = data.get("count")
    if pile is None or count is None:
        return jsonify({"error": "pile and count required"}), 400

    # validate
    if pile < 0 or pile >= len(game["piles"]) or count < 1 or count > game["piles"][pile]:
        return jsonify({"error": "Invalid move"}), 400

    # Apply move
    game["piles"][pile] -= count
    game["player"] = 0 if game["player"] == 1 else 1

    if all(p == 0 for p in game["piles"]):
        game["winner"] = game["player"]  # other player just won

    return jsonify({"state": serialize_game_state(game)})


@app.route("/api/ai-move/<game_id>", methods=["POST"])
def ai_move(game_id):
    """
    Triggers the AI to make a move in the specified game.
    The AI uses the global AI object (loaded/trained).
    Returns the move taken and updated state.
    """
    game = GAMES.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    if game["winner"] is not None:
        return jsonify({"error": "game finished", "state": serialize_game_state(game)}), 400

    # If no valid moves, return error
    available = Nim.available_actions(tuple(game["piles"]))
    if not available:
        game["winner"] = game["player"]
        return jsonify({"error": "no moves available", "state": serialize_game_state(game)}), 400

    # choose action using AI (no epsilon for deterministic move)
    pile, count = AI.choose_action(game["piles"], epsilon=False)
    # validate chosen action
    if (pile, count) not in available:
        # fallback: pick random valid
        pile, count = random.choice(list(available))

    # apply
    game["piles"][pile] -= count
    game["player"] = 0 if game["player"] == 1 else 1
    if all(p == 0 for p in game["piles"]):
        game["winner"] = game["player"]

    return jsonify({"move": {"pile": pile, "count": count}, "state": serialize_game_state(game)})


@app.route("/api/train", methods=["POST"])
def train_ai():
    """
    Body JSON: { "games": 1000 }  -> train AI synchronously (blocking).
    WARNING: This runs in-process and will block the server while training.
    """
    data = request.get_json() or {}
    n = int(data.get("games", 1000))
    # very small safety cap:
    if n <= 0 or n > 200000:
        return jsonify({"error": "invalid games number"}), 400

    # train (blocking)
    new_ai = train(n)
    # save
    try:
        with open(AI_PATH, "wb") as f:
            pickle.dump(new_ai, f)
    except Exception as e:
        print("Failed to save AI:", e)

    global AI
    AI = new_ai
    return jsonify({"status": "trained", "games": n}), 200


# Serve react app (production)
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    # If path is a file in the build, serve it; otherwise serve index.html
    if path != "" and os.path.exists(os.path.join(BUILD_DIR, path)):
        return send_from_directory(BUILD_DIR, path)
    index_path = os.path.join(BUILD_DIR, "index.html")
    if os.path.exists(index_path):
        return send_from_directory(BUILD_DIR, "index.html")
    return jsonify({"message": "No frontend build found. Run `npm run build` in frontend/`."}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
