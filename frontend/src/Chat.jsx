import React, { useState, useEffect, useRef } from "react";
import { sendMessageStream, getHistory } from "./api";

function Chat({ token, setToken }) {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    loadHistory();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const loadHistory = async () => {
    const data = await getHistory(token);
    if (Array.isArray(data)) {
      setMessages(data);
    }
  };

  const handleSend = async () => {
    if (!message.trim()) return;

    const userMessage = { role: "user", content: message };
    const assistantPlaceholder = { role: "assistant", content: "" };

    setMessages(prev => [...prev, userMessage, assistantPlaceholder]);
    setMessage("");
    setLoading(true);

    await sendMessageStream(message, token, (chunk) => {
      setMessages(prev => {
        const updated = [...prev];
        updated[updated.length - 1].content += chunk;
        return updated;
      });
    });

    setLoading(false);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h2>AI Personal Assistant</h2>
        <button style={styles.logoutBtn} onClick={handleLogout}>
          Logout
        </button>
      </div>

      <div style={styles.chatBox}>
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              ...styles.message,
              alignSelf: msg.role === "user" ? "flex-end" : "flex-start",
              backgroundColor:
                msg.role === "user" ? "#2563eb" : "#e5e7eb",
              color: msg.role === "user" ? "white" : "black"
            }}
          >
            {msg.content}
          </div>
        ))}

        {loading && (
          <div style={styles.typingIndicator}>
            AI is typing...
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      <div style={styles.inputArea}>
        <input
          style={styles.input}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type a message..."
        />
        <button style={styles.sendBtn} onClick={handleSend}>
          Send
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    width: "800px",
    margin: "40px auto",
    display: "flex",
    flexDirection: "column",
    fontFamily: "Arial"
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    marginBottom: "15px"
  },
  logoutBtn: {
    padding: "6px 12px",
    backgroundColor: "#ef4444",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer"
  },
  chatBox: {
    height: "500px",
    display: "flex",
    flexDirection: "column",
    overflowY: "auto",
    border: "1px solid #ddd",
    borderRadius: "10px",
    padding: "15px",
    backgroundColor: "#f9fafb"
  },
  message: {
    padding: "10px 14px",
    borderRadius: "12px",
    marginBottom: "10px",
    maxWidth: "70%"
  },
  inputArea: {
    display: "flex",
    marginTop: "10px"
  },
  input: {
    flex: 1,
    padding: "10px",
    borderRadius: "6px",
    border: "1px solid #ccc"
  },
  sendBtn: {
    marginLeft: "10px",
    padding: "10px 20px",
    backgroundColor: "#10b981",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer"
  },
  typingIndicator: {
    fontStyle: "italic",
    color: "gray"
  }
};

export default Chat;
