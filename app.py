import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def get_advanced_driver():
    options = Options()
    # دروستکردنی ناسنامەی جیاواز بۆ تێپەڕاندنی سیکیوریتی
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    ]
    options.add_argument(f'user-agent={random.choice(user_agents)}')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # بەکارهێنانی وێبگەڕ بەبێ ئەوەی پشانت بدات (Headless) ئەگەر ویستت
    # options.add_argument("--headless") 

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def check_site(email, site_url, input_id):
    driver = get_advanced_driver()
    try:
        driver.get(site_url)
        time.sleep(random.uniform(2, 5)) # وەستان بۆ ئەوەی وەک ڕۆبۆت دەرنەکەوێت
        
        search_input = driver.find_element(By.ID, input_id)
        search_input.send_keys(email)
        time.sleep(1)
        
        # لێرەدا دەتوانیت پشکنین بکەیت ئەگەر وەڵامی سایتەکە وتی ئیمێڵەکە هەیە
        print(f"[*] Checking {site_url} for {email}...")
        
        # تێبینی: هەر سایتێک Logic ی خۆی هەیە بۆ پشکنین
        # ئەمە وەک نموونەیە بۆ تێپەڕاندنی سیکیوریتی سەرەتایی
        
    except Exception as e:
        print(f"[!] Error checking {site_url}: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    email = input("Target Email: ")
    # نموونەی پشکنین بۆ سایتێکی دیاریکراو
    check_site(email, "https://accounts.google.com/", "identifierId")
