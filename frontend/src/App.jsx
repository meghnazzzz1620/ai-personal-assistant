import React, { useState } from "react";
import Login from "./Login";
import Chat from "./Chat";
import Admin from "./Admin";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [view, setView] = useState("chat");

  if (!token) {
    return <Login setToken={setToken} />;
  }

  return (
    <div>
      <div style={{ textAlign: "center", margin: "10px" }}>
        <button onClick={() => setView("chat")}>Chat</button>
        <button onClick={() => setView("admin")}>Admin</button>
      </div>

      {view === "chat" ? (
        <Chat token={token} setToken={setToken} />
      ) : (
        <Admin token={token} />
      )}
    </div>
  );
}

export default App;
