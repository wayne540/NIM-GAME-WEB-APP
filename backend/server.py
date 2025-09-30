# backend/server.py
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")
CORS(app)

# Example in-memory game storage
games = {}
game_counter = 0

# API to create a new game
@app.route("/api/new-game", methods=["POST"])
def new_game():
    global game_counter
    data = request.get_json()
    initial = data.get("initial", [1, 3, 5, 7])
    mode = data.get("mode", "normal")
    ai_player = data.get("ai_player", None)

    game_id = str(game_counter)
    game_counter += 1

    games[game_id] = {
        "game_id": game_id,
        "state": {
            "piles": initial,
            "player": 0,
            "winner": None,
            "mode": mode,
            "ai_player": ai_player
        }
    }

    return jsonify(games[game_id])

# API to make a move
@app.route("/api/move/<game_id>", methods=["POST"])
def make_move(game_id):
    game = games.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404

    data = request.get_json()
    pile = data.get("pile")
    count = data.get("count", 1)
    piles = game["state"]["piles"]

    if pile is None or pile >= len(piles) or piles[pile] < count:
        return jsonify({"error": "Invalid move"}), 400

    piles[pile] -= count
    if sum(piles) == 0:
        game["state"]["winner"] = game["state"]["player"]
    else:
        game["state"]["player"] = 1 - game["state"]["player"]

    return jsonify({"state": game["state"]})

# API for AI move (simple random)
@app.route("/api/ai-move/<game_id>", methods=["POST"])
def ai_move(game_id):
    import random
    game = games.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404

    piles = game["state"]["piles"]
    non_empty = [i for i, p in enumerate(piles) if p > 0]
    if not non_empty:
        return jsonify({"error": "Game over"}), 400

    pile = random.choice(non_empty)
    count = random.randint(1, piles[pile])
    piles[pile] -= count
    if sum(piles) == 0:
        game["state"]["winner"] = game["state"]["player"]
    else:
        game["state"]["player"] = 1 - game["state"]["player"]

    return jsonify({"state": game["state"]})

# Serve React frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
