from fastapi import APIRouter, Query
import pymysql
import googlemaps
import re
import math
from src.database import get_db_connection
from src.config import GOOGLE_MAPS_API_KEY

router = APIRouter()

# ✅ Google Maps API Key (Replace with your real API key)
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

# ✅ Haversine Formula to Calculate Distance (KM)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in KM
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@router.get("/chatbot")
def chatbot(query: str = Query(..., title="User Query")):
    """Handles user queries about Subway outlets."""
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query_lower = query.lower()

    # ✅ Handle "Find me outlets near [location]"
    match = re.search(r"near\s+([\w\s]+)", query_lower)
    if match:
        location = match.group(1).strip()
        try:
            # ✅ Geocode location
            geocode_result = gmaps.geocode(location)
            if not geocode_result:
                return {"message": f"❌ No results found for {location}"}

            loc_lat = geocode_result[0]["geometry"]["location"]["lat"]
            loc_lon = geocode_result[0]["geometry"]["location"]["lng"]

            # ✅ Fetch all outlets
            cursor.execute("SELECT id, name, address, hours, waze_link, latitude, longitude FROM outlets")
            outlets = cursor.fetchall()

            # ✅ Find nearby outlets within 5KM
            nearby_outlets = [
                outlet for outlet in outlets if haversine(loc_lat, loc_lon, outlet["latitude"], outlet["longitude"]) <= 5
            ]

            if not nearby_outlets:
                return {"message": f"🚫 No Subway outlets found within 5KM of {location}"}
            
            return {"message": f"✅ Outlets near {location}:", "data": nearby_outlets}

        except Exception as e:
            return {"message": f"❌ Error finding outlets near {location}: {str(e)}"}

    # ✅ Find outlets that close the latest
    elif "close" in query_lower and ("latest" in query_lower or "last" in query_lower):
        cursor.execute("SELECT name, address, hours, waze_link, latitude, longitude FROM outlets ORDER BY hours DESC LIMIT 5")
        results = cursor.fetchall()
        return {"message": "These outlets close the latest:", "data": results}

    # ✅ Count outlets in a specific location
    elif "how many" in query_lower:
        location_match = re.findall(r"how many outlets in\s+([\w\s\.]+)", query_lower)
        if location_match:
            location = location_match[0].strip()
            if location.lower() in ["kl", "k.l"]:
                location = "Kuala Lumpur"
            search_location = f"%{location.lower()}%"

            cursor.execute("""
                SELECT name, address, hours, waze_link, latitude, longitude
                FROM outlets
                WHERE LOWER(TRIM(address)) LIKE LOWER(%s)
            """, (search_location,))
            results = cursor.fetchall()

            if results:
                return {
                    "message": f"✅ There are {len(results)} Subway outlets in {location}.",
                    "data": results
                }
            else:
                return {"message": f"❌ No Subway outlets found in {location} (Check Address Format!)"}

    return {"message": "❌ I didn't understand your question. Try asking about outlet hours, locations, or nearest Subway."}
