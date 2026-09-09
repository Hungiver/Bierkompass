import json
import requests
from datetime import datetime

def fetch_live_deals():
    deals = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    # 1. BILLA & PENNY VALÓS API LEKÉRDEZÉS
    try:
        url = "https://shop.billa.at/api/general/search?searchTerm=Bier&pageSize=50"
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            for prod in data.get("tiles", []):
                # Csak az akciós termékeket szűrjük ki
                if prod.get("price", {}).get("isDiscounted"):
                    name = prod.get("name", "")
                    price = prod.get("price", {}).get("regular", {}).get("value", 0)
                    deals.append({
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "store": "BILLA",
                        "distance": 2.0,
                        "beer": "Puntigamer" if "Puntigamer" in name else "Wieselburger" if "Wieselburger" in name else "Bier",
                        "name": name,
                        "price": f"{price} €",
                        "origPrice": "Akció",
                        "note": "Billa Live"
                    })
    except Exception as e:
        print(f"Billa hiba: {e}")

    # 2. SPAR VALÓS KERESŐ API
    try:
        spar_url = "https://www.interspar.at/store/api/v1/products?q=Bier&isSale=true"
        res = requests.get(spar_url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            for prod in data.get("products", []):
                deals.append({
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "store": "SPAR",
                    "distance": 1.8,
                    "beer": prod.get("brand", "Bier"),
                    "name": prod.get("name", ""),
                    "price": f"{prod.get('price', 0)} €",
                    "origPrice": "Akció",
                    "note": "Spar Live"
                })
    except Exception as e:
        print(f"Spar hiba: {e}")

    # Eredmények mentése
    with open("deals.json", "w", encoding="utf-8") as f:
        json.dump(deals, f, ensure_ascii=False, indent=2)

    print(f"Kész! {len(deals)} db valós élő akció letöltve.")

if __name__ == "__main__":
    fetch_live_deals()
