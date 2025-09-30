// frontend/src/App.jsx
import React, { useState } from "react";
import Menu from "./components/Menu";
import GameBoard from "./components/GameBoard";
import HUD from "./components/HUD";

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
        <div>
          <button onClick={() => setPage("menu")} style={{ margin: 8 }}>
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
