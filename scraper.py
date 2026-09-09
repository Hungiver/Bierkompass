import json
import requests
from datetime import datetime, timedelta

def fetch_deals():
    deals = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # 1. PENNY AT API
    try:
        penny_url = "https://www.penny.at/api/products?category=bier" # Példa belső végpont
        res = requests.get(penny_url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            for item in data.get("results", []):
                if "Puntingamer" in item.get("name", "") or "Schwechater" in item.get("name", ""):
                    deals.append({
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "store": "PENNY",
                        "distance": 1.5,
                        "beer": "Puntingamer" if "Puntingamer" in item["name"] else "Schwechater",
                        "name": item.get("name"),
                        "price": f"{item.get('price', 0) / 100:.2f} €",
                        "origPrice": f"{item.get('regularPrice', 0) / 100:.2f} €",
                        "note": "Penny Akció"
                    })
    except Exception as e:
        print(f"Penny hiba: {e}")

    # 2. HOFER AT API
    try:
        hofer_url = "https://www.hofer.at/api/v1/products/offers"
        res = requests.get(hofer_url, headers=headers, timeout=10)
        if res.status_code == 200:
            # Hofer termékek feldolgozása
            pass
    except Exception as e:
        print(f"Hofer hiba: {e}")

    # Mentés deals.json-ba
    with open("deals.json", "w", encoding="utf-8") as f:
        json.dump(deals, f, ensure_ascii=False, indent=2)

    print("Frissítés kész!")

if __name__ == "__main__":
    fetch_deals()
