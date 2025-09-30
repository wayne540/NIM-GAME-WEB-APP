// frontend/src/components/HUD.jsx
import React from "react";

export default function HUD({ game }) {
  const state = game.state;
  return (
    <div style={{ padding: 12, borderBottom: "1px solid #ddd" }}>
      <div>Turn: Player {state.player}</div>
      <div>Winner: {state.winner === null ? "—" : `Player ${state.winner}`}</div>
      <div>Mode: {state.mode}</div>
    </div>
  );
}
