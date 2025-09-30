# Nim AI Web App

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Project Structure](#project-structure)
5. [Frontend Details](#frontend-details)
6. [Backend Details](#backend-details)
7. [AI Implementation](#ai-implementation)
8. [Installation & Setup](#installation--setup)
9. [Running Locally](#running-locally)
10. [Deployment](#deployment)
11. [Usage Guide](#usage-guide)
12. [Folder/File Descriptions](#folderfile-descriptions)
13. [Troubleshooting & FAQs](#troubleshooting--faqs)
14. [Contributing](#contributing)
15. [License](#license)
16. [Acknowledgements](#acknowledgements)

---

## Project Overview

The **Nim AI Web App** is an interactive web application that allows users to play the classic mathematical strategy game **Nim** against a computer AI or a human opponent. The game has been implemented with **React** on the frontend for a responsive and engaging UI, and **Flask** on the backend to manage game state, handle AI moves, and provide an API for communication between the frontend and backend.

This project was designed not only as a fun game but also as a demonstration of **AI decision-making**, **full-stack development**, and **modern web application deployment**. The AI uses **Q-learning**, a reinforcement learning algorithm, to learn optimal strategies for winning the game over multiple training sessions.

Players can customize the game by setting the initial piles, choosing the game mode (Normal or Misère), and deciding whether they want the AI to play as Player 0, Player 1, or not at all.

---

## Features

* **Multiplayer Mode**: Play against another human locally.
* **AI Mode**: Challenge the AI that learns optimal moves via reinforcement learning.
* **Custom Game Settings**: Define the initial piles (e.g., `[1,3,5,7]`) and choose game mode.
* **Dynamic Game Board**: Visually represents piles and counters for an intuitive experience.
* **Turn-Based Gameplay**: Clearly indicates whose turn it is with a status HUD.
* **Real-Time AI Moves**: Ask the AI to make a move instantly during gameplay.
* **Web-Friendly**: Fully responsive design for desktop, tablet, and mobile browsers.
* **Offline Fallback**: The app is a Progressive Web App (PWA), allowing offline play for cached games.
* **Persistent AI**: Trains and stores AI strategies for consistent performance across sessions.
* **User-Friendly Interface**: Simple menus, clear controls, and interactive game elements.

---

## Technologies Used

The project leverages modern frontend and backend technologies:

* **Frontend**:

  * React 18
  * HTML5 & CSS3
  * JavaScript (ES6+)
  * CSS Modules for component-based styling
  * React Hooks (`useState`) for state management
* **Backend**:

  * Python 3.11+
  * Flask for REST API
  * Flask-CORS to handle cross-origin requests
  * Pickle for AI state persistence
* **AI Implementation**:

  * Q-learning algorithm
  * Reinforcement learning principles
* **Deployment Tools**:

  * Gunicorn (production WSGI server)
  * Node.js & npm for frontend build management
  * Optional: Docker for containerized deployment
* **Utilities**:

  * Pillow (PIL) for dynamic favicon creation

---

## Project Structure

```
NIM-GAME-WEB-APP/
├─ backend/
│  ├─ server.py           # Flask API backend
│  ├─ nim.py              # Game logic + AI implementation
│  ├─ nim_ai.pkl          # Pickle file storing trained AI
│  ├─ requirements.txt    # Python dependencies
│  └─ make_favicon.py     # Script to generate favicon
├─ frontend/
│  ├─ public/
│  │  ├─ index.html
│  │  ├─ manifest.json
│  │  └─ favicon.png
│  ├─ src/
│  │  ├─ App.jsx
│  │  ├─ index.js
│  │  ├─ components/
│  │  │  ├─ GameBoard.jsx
│  │  │  ├─ HUD.jsx
│  │  │  └─ Menu.jsx
│  │  └─ styles/
│  │     ├─ global.css
│  │     ├─ GameBoard.css
│  │     ├─ HUD.css
│  │     └─ Menu.css
│  └─ package.json
├─ README.md
└─ .gitignore
```

---

## Frontend Details

The frontend is built using **React**. It features three primary components:

1. **Menu**:

   * Allows players to create a new game.
   * Lets users customize pile sizes, game mode, and AI participation.
   * Provides clear input fields and dropdowns for easy interaction.

2. **GameBoard**:

   * Displays the piles visually.
   * Interactive counters represent objects in each pile.
   * Clicking a pile selects it, and players can specify the number of objects to remove.
   * Buttons allow users to make moves or ask the AI to move.

3. **HUD (Heads-Up Display)**:

   * Shows current turn.
   * Displays the winner when the game ends.
   * Indicates the selected mode.

The global styling is centralized in **global.css**, while component-specific styles remain modular in their respective CSS files (`GameBoard.css`, `HUD.css`, `Menu.css`). This allows for easy maintenance and future UI updates.

---

## Backend Details

The backend is a **Flask API** serving two main purposes:

1. **Game Management**:

   * Maintains all active game sessions in memory with unique `game_id`s.
   * Tracks player turns and pile states.
   * Validates moves and ensures rules are followed.
   * Provides endpoints:

     * `POST /api/new-game` → create a new game
     * `GET /api/state/<game_id>` → get current game state
     * `POST /api/move/<game_id>` → make a move
     * `POST /api/ai-move/<game_id>` → AI makes a move
     * `POST /api/train` → train AI via reinforcement learning

2. **AI Training**:

   * Uses Q-learning stored in a dictionary mapping `(state, action)` → `Q-value`.
   * `train(n)` plays `n` self-games and updates Q-values based on rewards.
   * AI state is persisted in `nim_ai.pkl`.

The backend also serves the React frontend build when deployed, allowing the app to be fully full-stack.

---

## AI Implementation

The AI is implemented using **reinforcement learning (Q-learning)**:

* **State Representation**:

  * Each state is a tuple representing remaining objects in each pile.
  * Example: `(1, 3, 5, 7)`.
* **Action Representation**:

  * Each action is a tuple `(pile_index, objects_removed)`.
* **Q-Learning Update Rule**:

  ```python
  Q(state, action) = old_Q + α * ((reward + max_future_Q) - old_Q)
  ```

  * `α` = learning rate
  * `reward` = +1 for winning, -1 for losing, 0 otherwise
  * `max_future_Q` = maximum Q-value of the next state
* **Move Selection**:

  * Epsilon-greedy policy: AI chooses the best-known move most of the time but sometimes explores randomly to improve learning.
* **Training**:

  * AI can train for thousands of games against itself.
  * Trained AI is stored in a pickle file for reuse.

---

## Installation & Setup

### Prerequisites:

* Node.js 18+ and npm
* Python 3.11+
* pip
* Optional: Virtualenv

### Steps:

1. **Clone the repository**:

```bash
git clone https://github.com/wayne540/NIM-GAME-WEB-APP.git
cd NIM-GAME-WEB-APP
```

2. **Setup backend**:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. **Setup frontend**:

```bash
cd ../frontend
npm install
```

4. **Generate favicon (optional)**:

```bash
python make_favicon.py
```

---

## Running Locally

1. **Start Flask backend**:

```bash
cd backend
python server.py
```

2. **Start React frontend**:

```bash
cd frontend
npm start
```

* Access the app at `http://localhost:3000`.
* API requests are proxied to `http://localhost:5000`.

---

## Deployment

You can deploy using **Heroku**, **DigitalOcean**, **Render**, or **Docker**.

### Example: Heroku Deployment

1. Install Heroku CLI.
2. Create a `Procfile`:

```
web: gunicorn server:app
```

3. Specify Python version:

`runtime.txt`:

```
python-3.11.6
```

4. Build frontend for production:

```bash
cd frontend
npm run build
```

5. Move build folder to backend if needed.
6. Push to Heroku:

```bash
git add .
git commit -m "Prepare for deployment"
git push heroku main
```

7. Open deployed app:

```bash
heroku open
```

---

## Usage Guide

1. Navigate to the **Menu** page.
2. Choose initial piles, mode, and AI settings.
3. Click **Create Game**.
4. The **GameBoard** page will appear:

   * Click a pile to select it.
   * Enter number of objects to remove.
   * Click **Make Move**.
5. Use **Ask AI to Move** to let the AI play its turn.
6. Check **HUD** for current player, winner, and mode.

---

## Folder/File Descriptions

* **backend/nim.py** → core game logic & AI.
* **backend/server.py** → Flask API and frontend serving.
* **frontend/src/components/** → React components for UI.
* **frontend/src/styles/** → CSS files, including global styling.
* **frontend/public/** → static assets (favicon, index.html, manifest.json).

---

## Troubleshooting & FAQs

* **Issue**: Game doesn’t start

  * **Fix**: Make sure backend is running (`server.py`) and React app is started (`npm start`).
* **Issue**: AI moves not updating

  * **Fix**: Check that the backend AI pickle file exists (`nim_ai.pkl`) and is accessible.
* **Issue**: Proxy errors

  * **Fix**: Ensure `package.json` proxy points to backend port (`5000`) and both servers run concurrently.

---

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m "Add feature"`).
4. Push to branch (`git push origin feature-name`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

* [React](https://reactjs.org/) – Frontend framework
* [Flask](https://flask.palletsprojects.com/) – Backend API framework
* [Python Pillow](https://pillow.readthedocs.io/) – Favicon creation
* Reinforcement learning concepts for AI implementation


