from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

# Flask app setup
app = Flask(
    __name__,
    static_folder="../frontend/build",  # React build output
    static_url_path="/"
)
CORS(app)


# ---------------------------
# API routes
# ---------------------------
@app.route("/api/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Hello from Flask backend!"})


# Example future game endpoints
@app.route("/api/create-game", methods=["POST"])
def create_game():
    data = request.json
    # Example response, replace with your game logic
    return jsonify({"game_id": 1, "state": "new"})


# ---------------------------
# Serve React frontend
# ---------------------------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    """
    If path exists in React build folder, serve it.
    Otherwise, return index.html (for React Router support).
    """
    build_dir = app.static_folder
    index_path = os.path.join(build_dir, "index.html")

    if path != "" and os.path.exists(os.path.join(build_dir, path)):
        return send_from_directory(build_dir, path)
    elif os.path.exists(index_path):
        return send_from_directory(build_dir, "index.html")
    else:
        return "React build not found. Run 'npm run build' in frontend.", 404


# ---------------------------
# Run the app
# ---------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # works locally & on Heroku/Render
    app.run(host="0.0.0.0", port=port)
