import pymysql
from src.config import DB_CONFIG

def get_db_connection():
    """Establish a database connection"""
    return pymysql.connect(**DB_CONFIG)
