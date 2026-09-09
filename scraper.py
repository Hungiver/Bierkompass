import json
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

def fetch_with_browser():
    deals = []
    
    with sync_playwright() as p:
        # Fej nélküli Chromium indítása valódi felhasználói adatokkal
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            locale="de-AT"
        )
        page = context.new_page()

        # BILLA / PENNY LEKÉRDEZÉS BÖNGÉSZŐVEL
        try:
            print("Billa megnyitása böngészővel...")
            page.goto("https://shop.billa.at/suche/bier", wait_until="networkidle", timeout=30000)
            time.sleep(3) # Várakozás a dinamikus betöltésre
            
            # Termékek kinyerése a DOM-ból
            products = page.query_selector_all("[data-testid='product-tile'], .product-tile, article")
            print(f"Billa talált elemek: {len(products)}")

            for prod in products:
                text = prod.inner_text()
                if "€" in text and any(b in text.lower() for b in ["bier", "puntigamer", "schwechater", "wieselburger", "ottakringer", "gösser"]):
                    lines = [line.strip() for line in text.split("\n") if line.strip()]
                    deals.append({
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "store": "BILLA",
                        "distance": 2.0,
                        "beer": lines[0] if lines else "Bier",
                        "name": " ".join(lines[:2]),
                        "price": next((l for l in lines if "€" in l), "N/A"),
                        "origPrice": "Akció",
                        "note": "Billa Live"
                    })
        except Exception as e:
            print(f"Billa Playwright hiba: {e}")

        browser.close()

    # Eredmények mentése
    with open("deals.json", "w", encoding="utf-8") as f:
        json.dump(deals, f, ensure_ascii=False, indent=2)

    print(f"Összesen kinyert akciók: {len(deals)}")

if __name__ == "__main__":
    fetch_with_browser()
