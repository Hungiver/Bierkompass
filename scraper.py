import json
import requests
from datetime import datetime

def fetch_live_deals():
    deals = []
    
    # Valódi böngészőt szimuláló fejlécek, hogy a szerverek ne blokkolják a GitHub Actiont
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "de-AT,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://shop.billa.at/"
    }

    # 1. BILLA / PENNY ÉLŐ LEKÉRDEZÉS
    try:
        url = "https://shop.billa.at/api/general/search?searchTerm=Bier&pageSize=100"
        session = requests.Session()
        res = session.get(url, headers=headers, timeout=15)
        
        if res.status_code == 200:
            data = res.json()
            tiles = data.get("tiles", [])
            for prod in tiles:
                # Szűrés akciós termékekre
                is_discounted = prod.get("price", {}).get("isDiscounted", False)
                name = prod.get("name", "")
                
                if is_discounted or any(b in name.lower() for b in ["puntigamer", "schwechater", "wieselburger", "ottakringer", "gösser"]):
                    price_val = prod.get("price", {}).get("regular", {}).get("value", 0) / 100
                    orig_val = prod.get("price", {}).get("normal", {}).get("value", 0) / 100 if prod.get("price", {}).get("normal") else price_val
                    
                    deals.append({
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "store": "BILLA",
                        "distance": 2.0,
                        "beer": name.split()[0],
                        "name": name,
                        "price": f"{price_val:.2f} €",
                        "origPrice": f"{orig_val:.2f} €" if orig_val > price_val else "Akció",
                        "note": "Billa Live"
                    })
    except Exception as e:
        print(f"Billa élő lekérdezési hiba: {e}")

    # Mentés a deals.json fájlba
    with open("deals.json", "w", encoding="utf-8") as f:
        json.dump(deals, f, ensure_ascii=False, indent=2)

    print(f"Lekérdezés kész. Találatok száma: {len(deals)}")

if __name__ == "__main__":
    fetch_live_deals()
