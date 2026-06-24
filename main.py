import time
import os
import datetime
from config import PRODUCT_URL, PRODUCT_NAME, CHECK_INTERVAL_SECONDS
from database import init_database, save_price_to_db
from parser import get_current_price
from inflation import print_inflation_report

def main_loop():
    init_database()
    print(f"\n🚀 Starting price monitoring for '{PRODUCT_NAME}'")
    print(f"⏱️ Check interval: {CHECK_INTERVAL_SECONDS} seconds")
    print(f"🔗 URL: {PRODUCT_URL}\n")
    
    iteration = 0
    while True:
        iteration += 1
        print(f"\n{'='*60}")
        print(f"🔄 Iteration #{iteration} - {datetime.datetime.now()}")
        print(f"{'='*60}")
        
        current_price = get_current_price(PRODUCT_URL)
        
        if current_price is not None:
            save_price_to_db(PRODUCT_NAME, current_price)
            print_inflation_report()
        else:
            print("⚠️ Could not get price in this iteration")
        
        print(f"\n⏳ Waiting {CHECK_INTERVAL_SECONDS} seconds...\n")
        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user")
        os._exit(0)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        os._exit(1)