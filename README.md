# 🚀 Subway Outlet Locator

A **Full-Stack Subway Outlet Locator** that allows users to:
- **View Subway locations on a map** with a **5KM coverage radius**.
- **Interact with a chatbot** to find outlets near a location.
- **Click an outlet in the chatbot** to highlight it on the map and show details in a popup.

## 📌 **Table of Contents**
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [Backend API (FastAPI)](#backend-api-fastapi)
- [Frontend (React)](#frontend-react)
- [Project Structure](#project-structure)
- [Future Improvements](#future-improvements)

---

## 🎯 **Features**
✅ **Web Scraping** - Extracts Subway outlet data from `subway.com.my/find-a-subway`.  
✅ **Database Storage** - Stores outlet details in **MySQL** (name, address, hours, latitude, longitude).  
✅ **Geolocation** - Uses **Google Maps API** to get coordinates for each outlet.  
✅ **FastAPI Backend** - Provides an API for outlets and chatbot responses.  
✅ **React Frontend** - Displays **interactive map with markers** using Leaflet.js.  
✅ **Chatbot Search** - Allows users to search for outlets near a specific location.  
✅ **Map Integration** - Clicking on a chatbot result **highlights** and **shows popup** on the map.  

---

## 🛠 **Tech Stack**
### **Backend**
- 🐍 **FastAPI** - High-performance Python web framework.
- 🛢 **MySQL** - Stores Subway outlet data.
- 🛰 **Google Maps API** - Geocodes outlet locations.
- 🤖 **Selenium** - Scrapes Subway website for outlet details.

### **Frontend**
- ⚛️ **React.js** - Frontend framework for UI.
- 🗺 **Leaflet.js** - Interactive maps & markers.
- 🔄 **Axios** - Handles API requests.
- 💬 **React Hooks** - Manages chatbot state.

---

## 🚀 **Setup Instructions**

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/subway-locator.git
cd subway-locator
```

### **2️⃣ Backend Setup (FastAPI)**
#### ✅ **Install Python Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

#### ✅ **Setup MySQL Database**
1. Create a **MySQL database** called `subway_db`.
2. Run the SQL script to create the `outlets` table:
```sql
CREATE TABLE outlets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    address TEXT,
    hours TEXT,
    waze_link TEXT,
    latitude FLOAT,
    longitude FLOAT
);
```

#### ✅ **Run the Backend API**
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
- The API will be available at: `http://localhost:8000/`
- Test it by opening: `http://localhost:8000/docs`

---

### **3️⃣ Frontend Setup (React)**
#### ✅ **Install Dependencies**
```bash
cd frontend
npm install
```

#### ✅ **Run the Frontend**
```bash
npm start
```
- The frontend will be available at: `http://localhost:3000/`

---

## 🔌 **Backend API (FastAPI)**
### 📍 **Get All Outlets**
**`GET /outlets`**  
Retrieves a list of all Subway outlets.

#### 🔹 **Example Response**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name": "Subway KLCC",
      "address": "Lot 1, KLCC, Kuala Lumpur",
      "hours": "10AM - 10PM",
      "waze_link": "https://waze.com/link-to-klcc",
      "latitude": 3.15785,
      "longitude": 101.7113
    }
  ]
}
```

---

### 🤖 **Chatbot Endpoint**
**`GET /chatbot?query=Find me outlets near Bukit Bintang`**  
Processes user queries and returns matching Subway locations.

#### 🔹 **Example Query**
```bash
http://localhost:8000/chatbot?query=Find%20me%20outlets%20near%20Bukit%20Bintang
```

#### 🔹 **Example Response**
```json
{
  "message": "✅ Outlets near Bukit Bintang:",
  "data": [
    {
      "name": "Subway Pavilion",
      "address": "Pavilion Mall, Bukit Bintang, Kuala Lumpur",
      "hours": "10AM - 10PM",
      "waze_link": "https://waze.com/link-to-pavilion",
      "latitude": 3.14785,
      "longitude": 101.7133
    }
  ]
}
```

---

## 🎨 **Frontend (React)**
### 📌 **Map Features**
- **Displays outlets** on an interactive map.
- **Highlights outlets within 5KM of each other**.
- **Clicking an outlet in chatbot opens a popup on the map**.

### 📌 **Chatbot Features**
- Users can type queries like:
  - `"Find me outlets near KL Sentral"`
  - `"How many outlets in Bangsar?"`
  - `"Which outlets close the latest?"`
- The chatbot **fetches API data** and **updates the map**.

---

## 📁 **Project Structure**
```
📦 Subway Outlet Locator
 ┣ 📂 backend
 ┃ ┣ 📂 Data 
 ┃ ┣ 📂 src
 ┃ ┃ ┣ 📜 __init__.py            # Package initializer
 ┃ ┃ ┣ 📜 chatbot.py             # Chatbot API logic
 ┃ ┃ ┣ 📜 config.py              # Configuration settings
 ┃ ┃ ┣ 📜 database.py            # Database connection module
 ┃ ┃ ┣ 📜 geocoder.py            # Google Maps Geocoding logic
 ┃ ┃ ┣ 📜 main.py                # FastAPI server
 ┃ ┃ ┣ 📜 scraper.py             # Web scraper using Selenium
 ┃ ┗ 📜 requirements.txt         # Backend dependencies
 ┣ 📂 frontend
 ┃ ┣ 📂 src
 ┃ ┃ ┣ 📂 components
 ┃ ┃ ┃ ┣ 📜 Chatbot.js           # Chatbot UI
 ┃ ┃ ┃ ┣ 📜 SubwayMap.js         # Interactive map
 ┃ ┃ ┣ 📜 App.js                 # Main React App
 ┃ ┃ ┣ 📜 index.js               # React entry point
 ┃ ┣ 📜 package.json             # Frontend dependencies
 ┗ 📜 README.md                  # Project documentation
```

---

## 🚀 **Future Improvements**
🔹 **Dark Mode Support**  
🔹 **Mobile Responsiveness**  
🔹 **Search Bar for Finding Outlets**  
🔹 **More Chatbot Queries (e.g., "Show 24/7 outlets")**  

---

## 🤝 **Contributing**
1. Fork the repository  
2. Create a new branch: `git checkout -b feature-branch`  
3. Commit changes: `git commit -m "Added new feature"`  
4. Push branch: `git push origin feature-branch`  
5. Submit a **Pull Request** 🎉  

---

## 📧 **Contact**
For questions or support, email:  
📩 `muhdamirulaiman07@gmail.com`  
