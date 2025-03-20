import React, { useState } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000/chatbot"; // FastAPI Backend

const Chatbot = ({ onSelectOutlet }) => {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query) return;
    setLoading(true);
    try {
      const res = await axios.get(`${API_URL}?query=${query}`);
      setResponse(res.data);
    } catch (error) {
      setResponse({ message: "❌ Error fetching response" });
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div style={{
      maxWidth: "450px",
      margin: "10px auto",
      padding: "15px",
      backgroundColor: "white",
      borderRadius: "10px",
      boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.1)",
    }}>
      <h2 style={{ fontSize: "22px", fontWeight: "bold", textAlign: "center" }}>
        🟢 Subway Chatbot
      </h2>
      <div style={{
        display: "flex",
        alignItems: "center",
        gap: "5px",
        marginBottom: "10px"
      }}>
        <input
          type="text"
          placeholder='Ask about Subway outlets...'
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          style={{
            flex: 1,
            padding: "10px",
            borderRadius: "5px",
            border: "1px solid #ccc",
            fontSize: "16px"
          }}
        />
        <button
          onClick={handleSearch}
          style={{
            width: "100px",
            height: "40px",
            borderRadius: "5px",
            border: "none",
            background: "#28a745",
            color: "#fff",
            cursor: "pointer",
            fontSize: "16px",
            fontWeight: "bold"
          }}
        >
          🔍 Search
        </button>
      </div>

      {loading && <p style={{ textAlign: "center", fontSize: "16px", fontWeight: "bold" }}>⏳ Loading...</p>}

      {response && (
        <div style={{
          marginTop: "10px",
          padding: "15px",
          background: "#f8f9fa",
          borderRadius: "8px",
          boxShadow: "0px 2px 5px rgba(0, 0, 0, 0.1)"
        }}>
          <p style={{
            fontWeight: "bold",
            color: response.message.includes("✅") ? "#28a745" : "#dc3545",
            fontSize: "18px",
            textAlign: "center"
          }}>
            {response.message}
          </p>

          {response.data && response.data.length > 0 ? (
            <ul style={{ listStyleType: "none", padding: 0, marginTop: "10px" }}>
              {response.data.map((outlet, index) => (
                <li key={index} 
                  onClick={() => onSelectOutlet(outlet)} 
                  style={{
                    cursor: "pointer",
                    padding: "10px",
                    borderBottom: "1px solid #ddd",
                    lineHeight: "1.5",
                    textAlign: "left",
                    transition: "0.3s",
                  }}
                >
                  <strong style={{ color: "#007bff" }}>📍 {outlet.name}</strong>
                  <br />
                  📌 {outlet.address}
                  <br />
                  🕒 {outlet.hours}
                  <br />
                  <a href={outlet.waze_link} target="_blank" rel="noopener noreferrer" style={{
                    color: "#ff5733",
                    textDecoration: "none",
                    fontWeight: "bold"
                  }}>
                    🚗 Open in Waze
                  </a>
                </li>
              ))}
            </ul>
          ) : (
            <p style={{ textAlign: "center", fontSize: "16px" }}>🚫 No outlets found.</p>
          )}
        </div>
      )}
    </div>
  );
};

export default Chatbot;
