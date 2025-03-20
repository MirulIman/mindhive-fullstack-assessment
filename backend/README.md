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
│── .env                  # Environment variables (DO NOT commit this!)
│── requirements.txt      # Dependencies list
│── README.md             # Project documentation
│── .gitignore            # Ignore unnecessary files
```

---

## ⚙️ Setup Instructions
### **1️⃣ Install Dependencies**
Make sure you have Python 3.8+ installed. Then, run:
```bash
pip install -r requirements.txt
```

### **2️⃣ Configure Environment Variables**
Create a `.env` file in the `backend/` directory with:
```ini
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=subway_db
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

### **3️⃣ Run Web Scraper**
Fetch Subway outlet data:
```bash
python src/scraper.py
```

### **4️⃣ Run Geocoder**
Retrieve latitude & longitude:
```bash
python src/geocoder.py
```

### **5️⃣ Start FastAPI Server**
Run the backend API:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```
Access it at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### **6️⃣ Test API**
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
