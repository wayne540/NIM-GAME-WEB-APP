// frontend/src/components/HUD.jsx
import React from "react";
import "../styles/HUD.css";

export default function HUD({ game }) {
  const state = game.state;
  return (
    <div className="hud">
      <h2>Game Status</h2>
      <div className="status">Turn: Player {state.player}</div>
      <div className="status">Winner: {state.winner === null ? "—" : `Player ${state.winner}`}</div>
      <div className="status">Mode: {state.mode}</div>
    </div>
  );
}
