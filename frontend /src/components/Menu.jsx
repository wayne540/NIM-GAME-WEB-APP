// frontend/src/components/Menu.jsx
import React, { useState } from "react";
import "../styles/GameBoard.css";

export default function Menu({ onCreate }) {
  const [initial, setInitial] = useState("1,3,5,7");
  const [mode, setMode] = useState("normal");
  const [aiPlayer, setAiPlayer] = useState(null);

  const createGame = async () => {
    const arr = initial.split(",").map((s) => parseInt(s.trim())).filter(n => !isNaN(n));
    const body = { initial: arr, mode, ai_player: aiPlayer };
    const res = await fetch("/api/new-game", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    const data = await res.json();
    onCreate(data);
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Nim — Create Game</h2>
      <label>Initial piles (comma separated)</label>
      <br />
      <input value={initial} onChange={e => setInitial(e.target.value)} style={{ width: 300 }} />
      <br />
      <label>Mode</label>
      <br />
      <select value={mode} onChange={e => setMode(e.target.value)}>
        <option value="normal">Normal</option>
        <option value="misere">Misère</option>
      </select>
      <br />
      <label>AI Player</label>
      <br />
      <select value={aiPlayer ?? ""} onChange={e => setAiPlayer(e.target.value === "" ? null : parseInt(e.target.value))}>
        <option value="">None (local/multiplayer)</option>
        <option value={0}>AI is Player 0 (goes first)</option>
        <option value={1}>AI is Player 1 (goes second)</option>
      </select>
      <br /><br />
      <button onClick={createGame}>Create Game</button>
    </div>
  );
}
