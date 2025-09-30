// frontend/src/App.jsx
import React, { useState } from "react";
import Menu from "./components/Menu";
import GameBoard from "./components/GameBoard";
import HUD from "./components/HUD";
import "./styles/global.css"; // make sure global styles are applied

function App() {
  const [page, setPage] = useState("menu"); // "menu" or "game"
  const [game, setGame] = useState(null);   // { game_id, state }

  return (
    <div className="app">
      {page === "menu" && (
        <Menu
          onCreate={(g) => {
            setGame(g);
            setPage("game");
          }}
        />
      )}

      {page === "game" && game && (
        <div className="game-page">
          <button className="back-button" onClick={() => setPage("menu")}>
            ← Back
          </button>
          <HUD game={game} setGame={setGame} />
          <GameBoard game={game} setGame={setGame} />
        </div>
      )}
    </div>
  );
}

export default App;
