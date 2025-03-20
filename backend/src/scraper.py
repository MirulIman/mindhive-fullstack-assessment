import pymysql
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import pandas as pd
from database import get_db_connection

# Ensure 'data' folder exists
data_folder = "data"
os.makedirs(data_folder, exist_ok=True)

# CSV file path
csv_file_path = os.path.join(data_folder, "subway_outlets.csv")

# Set up Selenium WebDriver
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_subway_outlets():
    driver.get("https://subway.com.my/find-a-subway")
    time.sleep(5)

    search_box = driver.find_element(By.ID, "fp_searchAddress")
    search_box.clear()
    search_box.send_keys("Kuala Lumpur")
    time.sleep(2)

    search_button = driver.find_element(By.ID, "fp_searchAddressBtn")
    search_button.click()
    time.sleep(5)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    outlet_elements = driver.find_elements(By.CLASS_NAME, "fp_listitem")
    outlet_data = []

    conn = get_db_connection()
    cursor = conn.cursor()

    for outlet in outlet_elements:
        try:
            name = outlet.find_element(By.TAG_NAME, "h4").text.strip()
            info_box = outlet.find_element(By.CLASS_NAME, "infoboxcontent")
            p_elements = info_box.find_elements(By.TAG_NAME, "p")
            address = p_elements[0].text.strip() if len(p_elements) > 0 else "N/A"
            hours = "\n".join([p.text.strip() for p in p_elements[1:]]) if len(p_elements) > 1 else "N/A"
            waze_links = outlet.find_elements(By.XPATH, ".//a[contains(@href, 'waze.com')]")
            waze_link = waze_links[0].get_attribute("href") if waze_links else "N/A"
            
            if "Kuala Lumpur" in address or "K.L" in address or "KL" in address:
                sql = """
                    INSERT INTO outlets (name, address, hours, waze_link)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE hours = VALUES(hours), waze_link = VALUES(waze_link);
                """
                cursor.execute(sql, (name, address, hours, waze_link))
                conn.commit()

                outlet_data.append({
                    "Name": name,
                    "Address": address,
                    "Hours": hours,
                    "Waze Link": waze_link
                })
        except Exception as e:
            print(f"Error extracting data: {e}")

    driver.quit()
    cursor.close()
    conn.close()

    df = pd.DataFrame(outlet_data)
    df.to_csv(csv_file_path, index=False, encoding="utf-8")
    print(f"Scraped {len(outlet_data)} outlets in Kuala Lumpur and stored in CSV and MySQL.")

if __name__ == "__main__":
    scrape_subway_outlets()
