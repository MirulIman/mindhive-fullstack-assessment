import React, { useState } from "react";
import SubwayMap from "./components/SubwayMap";
import Chatbot from "./components/Chatbot";

const App = () => {
  const [selectedOutlet, setSelectedOutlet] = useState(null); // ✅ Track selected outlet

  return (
    <div style={{ display: "flex", height: "96vh" }}>
      <div style={{ width: "28%", height: "100%", padding: "10px", backgroundColor: "#f8f9fa", overflowY: "auto"}}>
        <Chatbot onSelectOutlet={setSelectedOutlet} /> {/* ✅ Pass function */}
      </div>
      <div style={{ flex: 1, height: "100vh"}}>
        <SubwayMap selectedOutlet={selectedOutlet} /> {/* ✅ Highlight selected outlet */}
      </div>
    </div>
  );
};

export default App;
