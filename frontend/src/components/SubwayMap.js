import React, { useEffect, useState, useRef } from "react";
import { MapContainer, TileLayer, Marker, Popup, Circle, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import axios from "axios";
import MarkerClusterGroup from "react-leaflet-cluster";

const API_URL = "http://localhost:8000/outlets";
const RADIUS = 5000;

const subwayIcon = new L.Icon({
  iconUrl: "/subway_marker.png",
  iconSize: [40, 50],
  iconAnchor: [20, 50],
  popupAnchor: [0, -50]
});

const SubwayMap = ({ selectedOutlet }) => {
  const [outlets, setOutlets] = useState([]);
  const [intersections, setIntersections] = useState(new Set());
  const markersRef = useRef({}); // ✅ Store references to markers

  useEffect(() => {
    axios.get(API_URL)
      .then(response => {
        setOutlets(response.data.data);
      })
      .catch(error => {
        console.error("❌ Error fetching outlets:", error);
      });
  }, []);

  useEffect(() => {
    const checkIntersections = () => {
      let intersectingOutlets = new Set();

      outlets.forEach((outletA, indexA) => {
        outlets.forEach((outletB, indexB) => {
          if (indexA !== indexB) {
            const distance = getDistance(outletA.latitude, outletA.longitude, outletB.latitude, outletB.longitude);
            if (distance <= 5) {
              intersectingOutlets.add(outletA.id);
              intersectingOutlets.add(outletB.id);
            }
          }
        });
      });

      setIntersections(intersectingOutlets);
    };

    if (outlets.length > 0) checkIntersections();
  }, [outlets]);

  // ✅ Haversine Formula to Calculate Distance (in KM)
  const getDistance = (lat1, lon1, lat2, lon2) => {
    const R = 6371;
    const dLat = (lat2 - lat1) * (Math.PI / 180);
    const dLon = (lon2 - lon1) * (Math.PI / 180);
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(lat1 * (Math.PI / 180)) * Math.cos(lat2 * (Math.PI / 180)) *
      Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  };

  return (
    <MapContainer center={[3.1390, 101.6869]} zoom={12} style={{ height: "100vh", width: "100%" }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

      {/* ✅ Move Map to Selected Outlet & Open Popup */}
      {selectedOutlet && <PanToSelectedOutlet selectedOutlet={selectedOutlet} markersRef={markersRef} />}

      <MarkerClusterGroup chunkedLoading maxClusterRadius={80}>
        {outlets.map(outlet => (
          <Marker
            key={outlet.id}
            position={[outlet.latitude, outlet.longitude]}
            icon={subwayIcon}
            ref={(marker) => {
              if (marker) markersRef.current[outlet.id] = marker;
            }}
          >
            <Popup>
              <strong>📍 {outlet.name}</strong><br />
              📌 {outlet.address}<br />
              🕒 {outlet.hours}<br />
              <a href={outlet.waze_link} target="_blank" rel="noopener noreferrer" style={{
                    display: "inline-flex",
                    alignItems: "center",
                    color: "#ff5733",
                    textDecoration: "none",
                    fontWeight: "bold",
                    marginTop: "5px"
                  }}>🚗 Open in Waze</a>
            </Popup>
          </Marker>
        ))}
      </MarkerClusterGroup>

      {/* ✅ Show 5KM Circles (Green for Normal, Red for Intersections) */}
      {outlets.map(outlet => (
        <Circle
          key={`circle-${outlet.id}`}
          center={[outlet.latitude, outlet.longitude]}
          radius={RADIUS}
          pathOptions={{
            color: intersections.has(outlet.id) ? "red" : "green",
            fillColor: intersections.has(outlet.id) ? "red" : "green",
            fillOpacity: 0.08,
            weight: 1,
            opacity: 0.5
          }}
        />
      ))}
    </MapContainer>
  );
};

// ✅ Function to Pan Map to Selected Outlet & Open Popup
const PanToSelectedOutlet = ({ selectedOutlet, markersRef }) => {
  const map = useMap();
  useEffect(() => {
    if (selectedOutlet) {
      map.setView([selectedOutlet.latitude, selectedOutlet.longitude], 15, { animate: true });

      // ✅ Open the popup of the selected outlet
      setTimeout(() => {
        const marker = markersRef.current[selectedOutlet.id];
        if (marker && marker.getPopup()) {
          marker.openPopup(); // ✅ Force popup to open
        }
      }, 500);
    }
  }, [selectedOutlet, map]);
  return null;
};

export default SubwayMap;
