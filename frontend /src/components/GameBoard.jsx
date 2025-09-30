// frontend/src/components/GameBoard.jsx
import React, { useState } from "react";
import "../styles/GameBoard.css";
import { BACKEND_URL } from "../config";

export default function GameBoard({ game, setGame }) {
  const [selectedPile, setSelectedPile] = useState(null);
  const [removeCount, setRemoveCount] = useState(1);

  const makeMove = async () => {
    if (selectedPile === null) return;
    const res = await fetch(`/api/move/${game.game_id}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pile: selectedPile, count: parseInt(removeCount) })
    });
    const data = await res.json();
    if (res.ok) {
      setGame(prev => ({ ...prev, state: data.state }));
      setSelectedPile(null);
    } else {
      alert(data.error || "Invalid move");
    }
  };

  const aiMove = async () => {
    const res = await fetch(`/api/ai-move/${game.game_id}`, { method: "POST" });
    const data = await res.json();
    if (res.ok) {
      setGame(prev => ({ ...prev, state: data.state }));
    } else {
      alert(data.error || "AI error");
    }
  };

  const piles = game.state.piles;

  return (
    <div className="game-board">
      {piles.map((count, i) => (
        <div
          key={i}
          className={`pile ${selectedPile === i ? "selected" : ""}`}
          onClick={() => { setSelectedPile(i); setRemoveCount(1); }}
        >
          <div>Pile {i}</div>
          {/* Show counters instead of plain number */}
          <div>
            {Array.from({ length: count }).map((_, idx) => (
              <div key={idx} className="counter"></div>
            ))}
          </div>
        </div>
      ))}

      <div className="controls">
        <label>Selected pile: {selectedPile === null ? "None" : selectedPile}</label>
        <br />
        <label>Remove count:</label>
        <input
          type="number"
          min="1"
          value={removeCount}
          onChange={e => setRemoveCount(e.target.value)}
        />
        <br />
        <button onClick={makeMove} disabled={selectedPile === null}>Make Move</button>
        <button onClick={aiMove} style={{ marginLeft: 8 }}>Ask AI to Move</button>
      </div>
    </div>
  );
}
