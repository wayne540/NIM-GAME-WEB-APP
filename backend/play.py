from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(
    __name__,
    static_folder="../frontend/build",  # Point to React build folder
    static_url_path="/"                # Serve React from root URL
)

CORS(app)

# ---------------------------
# Example API route
# ---------------------------
@app.route("/api/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Hello from Flask backend!"})


# ---------------------------
# Serve React frontend
# ---------------------------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    """
    If path exists in build folder, serve it.
    Otherwise, serve index.html (so React Router works).
    """
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


# ---------------------------
# Run the app
# ---------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # works on Heroku/Render
    app.run(host="0.0.0.0", port=port)
