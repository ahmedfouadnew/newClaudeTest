import { useState, useEffect, useRef } from "react";
import "./App.css";

const API = "http://localhost:8000";

export default function App() {
  const [seasons, setSeasons] = useState([]);
  const [selectedSeason, setSelectedSeason] = useState("");
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    fetch(`${API}/seasons`)
      .then((r) => r.json())
      .then(setSeasons)
      .catch(() => {});
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function sendMessage(e) {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = { role: "user", content: input.trim() };
    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: updatedMessages,
          season_id: selectedSeason || null,
        }),
      });

      if (!res.ok) throw new Error("API error");
      const data = await res.json();
      setMessages([...updatedMessages, { role: "assistant", content: data.response }]);
    } catch {
      setMessages([
        ...updatedMessages,
        { role: "assistant", content: "Error: could not reach the server. Make sure the backend is running." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  const currentSeason = seasons.find((s) => s.id === selectedSeason);

  return (
    <div className="app">
      <header className="header">
        <div className="header-title">
          <h1>FRC / FTC Assistant</h1>
        </div>
        <select
          className="season-select"
          value={selectedSeason}
          onChange={(e) => {
            setSelectedSeason(e.target.value);
            setMessages([]);
          }}
        >
          <option value="">— General (no season) —</option>
          <optgroup label="FRC">
            {seasons.filter((s) => s.type === "FRC").map((s) => (
              <option key={s.id} value={s.id}>{s.name}</option>
            ))}
          </optgroup>
          <optgroup label="FTC">
            {seasons.filter((s) => s.type === "FTC").map((s) => (
              <option key={s.id} value={s.id}>{s.name}</option>
            ))}
          </optgroup>
        </select>
      </header>

      {currentSeason && (
        <div className="season-badge">
          Season: <strong>{currentSeason.name}</strong>
        </div>
      )}

      <div className="chat-window">
        {messages.length === 0 && (
          <div className="empty-state">
            <p>Ask anything about robot design, programming, or game strategy.</p>
            {!selectedSeason && <p className="hint">Select a season above for season-specific answers.</p>}
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`message ${m.role}`}>
            <div className="bubble">{m.content}</div>
          </div>
        ))}
        {loading && (
          <div className="message assistant">
            <div className="bubble thinking">Thinking…</div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <form className="input-bar" onSubmit={sendMessage}>
        <input
          type="text"
          placeholder="Ask about mechanisms, code, strategy…"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
          autoFocus
        />
        <button type="submit" disabled={loading || !input.trim()}>Send</button>
      </form>
    </div>
  );
}
