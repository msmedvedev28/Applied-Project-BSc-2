import time
import re
import json
from typing import Optional
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

def extract_price_from_text(text: str) -> Optional[float]:
    patterns = [
        r'(\d+[.,]\d{2})\s*[₽руб]?',
        r'(\d+[.,]\d{1,2})\s*[₽руб]',
        r'(\d+)\s*[₽руб]'
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            price_str = match.replace(',', '.')
            try:
                price = float(price_str)
                if 10 < price < 500:
                    return price
            except ValueError:
                continue
    return None

def get_current_price(url: str) -> Optional[float]:
    driver = None
    try:
        print("\n🟢 Opening browser...")
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        driver = uc.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print(f"📍 Loading page: {url}")
        driver.get(url)
        time.sleep(5)
        
        # Способ 1: По классу price
        print("🔍 Method 1: Looking for current price...")
        price_elements = driver.find_elements(By.CSS_SELECTOR, "div[class*='price']")
        for elem in price_elements:
            text = elem.text.strip()
            if text and 'Скидка' not in text:
                price = extract_price_from_text(text)
                if price:
                    print(f"✅ Price found: {price} ₽")
                    return price
        
        # Способ 2: JSON-LD
        print("🔍 Method 2: Looking for JSON-LD...")
        scripts = driver.find_elements(By.CSS_SELECTOR, "script[type='application/ld+json']")
        for script in scripts:
            try:
                data = json.loads(script.get_attribute('innerHTML'))
                if 'offers' in data:
                    offers = data['offers']
                    if isinstance(offers, dict) and 'price' in offers:
                        price = float(offers['price'])
                        if 10 < price < 500:
                            print(f"✅ Price from JSON-LD: {price} ₽")
                            return price
            except:
                continue
        
        # Способ 3: Полный текст страницы
        print("🔍 Method 3: Searching page text...")
        body_text = driver.find_element(By.TAG_NAME, "body").text
        all_prices = re.findall(r'(\d+[.,]\d{2})\s*[₽руб]', body_text)
        valid_prices = [float(p.replace(',', '.')) for p in all_prices if 10 < float(p.replace(',', '.')) < 500]
        
        if valid_prices:
            price = min(valid_prices)
            print(f"✅ Price from page text: {price} ₽")
            return price
        
        print("❌ Could not find price")
        return None
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None
        
    finally:
        if driver:
            input("\n📌 Press Enter to close browser...")
            driver.quit()