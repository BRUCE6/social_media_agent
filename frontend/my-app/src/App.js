import React, { useState } from "react";

function App() {
  const [messages, setMessages] = useState([
    { from: "agent", text: "Hello! Ask me to suggest or manage posts." },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { from: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("https://fuzzy-adventure-6rgwrw6pr6w25jgw-8000.app.github.dev/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await res.json();
      if (res.ok) {
        setMessages((prev) => [...prev, { from: "agent", text: data.response }]);
      } else {
        setMessages((prev) => [...prev, { from: "agent", text: `Error: ${data.detail}` }]);
      }
    } catch (e) {
      setMessages((prev) => [...prev, { from: "agent", text: "Error: Could not reach server." }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <div style={{ maxWidth: 600, margin: "20px auto", fontFamily: "Arial, sans-serif" }}>
      <h1>Post Management Chat</h1>
      <div
        style={{
          border: "1px solid #ccc",
          borderRadius: 5,
          padding: 10,
          height: 400,
          overflowY: "auto",
          marginBottom: 10,
          backgroundColor: "#f9f9f9",
        }}
      >
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{
              textAlign: msg.from === "user" ? "right" : "left",
              margin: "10px 0",
            }}
          >
            <div
              style={{
                display: "inline-block",
                padding: "8px 12px",
                borderRadius: 15,
                backgroundColor: msg.from === "user" ? "#007bff" : "#e5e5ea",
                color: msg.from === "user" ? "white" : "black",
                maxWidth: "80%",
                wordWrap: "break-word",
              }}
            >
              {msg.text}
            </div>
          </div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        placeholder="Type your message..."
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={handleKeyPress}
        disabled={loading}
        style={{ width: "100%", padding: 10, fontSize: 16, borderRadius: 5, border: "1px solid #ccc" }}
      />
      <button
        onClick={sendMessage}
        disabled={loading}
        style={{
          marginTop: 10,
          padding: "10px 20px",
          fontSize: 16,
          borderRadius: 5,
          border: "none",
          backgroundColor: "#007bff",
          color: "white",
          cursor: "pointer",
          width: "100%",
        }}
      >
        {loading ? "Sending..." : "Send"}
      </button>
    </div>
  );
}

export default App;