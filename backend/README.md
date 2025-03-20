# 🚀 Subway Outlets Locator - Backend

This project is a **FastAPI-based backend** that scrapes Subway outlets from `subway.com.my`, retrieves their geographical coordinates, and serves them via an API.

## 📁 Project Structure
```
backend/
│── src/
│   ├── __init__.py       # Package initializer
│   ├── main.py           # FastAPI server
│   ├── chatbot.py        # Chatbot API logic
│   ├── scraper.py        # Web scraper using Selenium
│   ├── geocoder.py       # Google Maps Geocoding logic
│   ├── database.py       # Database connection module
│   ├── config.py         # Configuration settings
│── data/                 # Stores scraped CSV data
│── requirements.txt      # Dependencies list
│── README.md             # Project documentation
```

---

## ⚙️ Setup Instructions
### **1️⃣ Install Dependencies**
Make sure you have Python 3.8+ installed. Then, run:
```bash
pip install -r requirements.txt
```

### **2️ Run Web Scraper**
Fetch Subway outlet data:
```bash
python src/scraper.py
```

### **3️ Run Geocoder**
Retrieve latitude & longitude:
```bash
python src/geocoder.py
```

### **4️ Start FastAPI Server**
Run the backend API:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```
Access it at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### **5️⃣ Test API**
Try these endpoints:
- **Get all outlets:** [`http://127.0.0.1:8000/outlets`](http://127.0.0.1:8000/outlets)
- **Chatbot Query:** [`http://127.0.0.1:8000/chatbot?query=how many outlets in Bangsar`](http://127.0.0.1:8000/chatbot?query=how%20many%20outlets%20in%20Bangsar)

---

## 🎯 Features
✔ Scrapes Subway outlets from `subway.com.my`
✔ Stores data in MySQL and CSV
✔ Retrieves GPS coordinates using Google Maps API
✔ Provides API to fetch outlet data
✔ Includes a chatbot for location-based queries

🚀 **Now your backend is ready to go!** 🚀
