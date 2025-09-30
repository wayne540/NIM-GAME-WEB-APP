// frontend/src/components/GameBoard.jsx
import React, { useState } from "react";

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
    <div style={{ padding: 20 }}>
      <h3>Game Board</h3>
      <div style={{ display: "flex", gap: 16 }}>
        {piles.map((count, i) => (
          <div key={i} style={{
            minWidth: 100, minHeight: 80, border: "1px solid #ccc", padding: 8,
            background: selectedPile === i ? "#eef" : "#fff", cursor: "pointer"
          }}
          onClick={() => { setSelectedPile(i); setRemoveCount(1); }}>
            <div>Pile {i}</div>
            <div style={{ fontSize: 24, marginTop: 8 }}>{count}</div>
          </div>
        ))}
      </div>

      <div style={{ marginTop: 12 }}>
        <label>Selected pile: {selectedPile === null ? "None" : selectedPile}</label>
        <br />
        <label>Remove count:</label>
        <input type="number" min="1" value={removeCount} onChange={e => setRemoveCount(e.target.value)} />
        <br />
        <button onClick={makeMove} disabled={selectedPile === null}>Make Move</button>
        <button onClick={aiMove} style={{ marginLeft: 8 }}>Ask AI to Move</button>
      </div>
    </div>
  );
}
