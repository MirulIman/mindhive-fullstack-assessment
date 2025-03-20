from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import get_db_connection
from src.chatbot import router as chatbot_router
import pymysql

app = FastAPI(title="Subway Outlets API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/outlets")
def get_outlets():
    """Fetch all Subway outlets"""
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT id, name, address, hours, waze_link, latitude, longitude FROM outlets")
    outlets = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"status": "success", "data": outlets}

# Include chatbot router
app.include_router(chatbot_router)
