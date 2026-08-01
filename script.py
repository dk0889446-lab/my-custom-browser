import os
import time
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def run_arolinks_fail_safe(url):
    proxy_host = "change4.owlproxy.com"
    proxy_port = "7778"
    proxy_user = "paCRkRTlf540_custom_zone_US_st__city_sid_01172404_time_5"
    proxy_pass = "5195429"
    
    proxy_options = {
        'proxy': {
            'http': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}',
            'https': f'http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}', 
            'no_proxy': 'localhost,127.0.0.1'
        },
        'verify_ssl': False
    }
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.page_load_strategy = 'normal'  
    
    # --- ANTI-BOT EVASION (VERY IMPORTANT) ---
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled") # Hides automation flag
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Hide WebRTC IP
    chrome_options.add_argument("--disable-webrtc")
    prefs = {
        "webrtc.ip_handling_policy": "disable_non_proxied_udp",
        "webrtc.multiple_routes_enabled": False,
        "webrtc.nonproxied_udp_enabled": False
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    print("[INFO] Initializing Stealth Chrome Driver...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options, seleniumwire_options=proxy_options)
    
    # --- JAVASCRIPT INJECTION TO HIDE SELENIUM ---
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })

    actions = ActionChains(driver)
    
    try:
        print("[PROXY] Setting up secure tunnel...")
        driver.get("https://icanhazip.com")
        time.sleep(3) 
        
        # [STEP 1] Target URL
        print(f"\n[STEP 1] Navigating to: {url}")
        driver.get(url)
        main_window = driver.current_window_handle
        time.sleep(10)
        
        # [STEP 3] Trigger Body
        try:
            driver.find_element(By.TAG_NAME, "body").click()
        except:
            pass

        # [STEP 4] Close Ads
        time.sleep(5)
        for window in driver.window_handles:
            if window != main_window:
                driver.switch_to.window(window)
                driver.close()
        driver.switch_to.window(main_window)
        time.sleep(12)
        
        # [STEP 6] Verify Button
        print("[STEP 6] Clicking 'Verify'...")
        verify_button = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Verify')] | //*[contains(text(), 'VERIFY')] | //button[contains(@id, 'verify')]")))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", verify_button)
        time.sleep(2)
        driver.execute_script("arguments[0].click();", verify_button) 
        
        # [STEP 7] Scroll Bottom
        time.sleep(2)
        driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
        time.sleep(3)

        # [STEP 8] Continue Button
        print("[STEP 8] Clicking 'Continue'...")
        continue_button = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Continue')] | //*[contains(text(), 'CONTINUE')]")))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", continue_button)
        time.sleep(2)
        driver.execute_script("arguments[0].click();", continue_button)
        
        # --- STAGE 2 ---
        print("\n[STAGE 2] Transitioning to final destination extraction layouts...")
        time.sleep(8) 

        for window in driver.window_handles:
            if window != main_window:
                driver.switch_to.window(window)
                driver.close()
        driver.switch_to.window(main_window)

        # Fake download close
        try:
            close_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Close'] | //button[contains(text(), 'Close')] | //span[contains(text(), 'Close')]")))
            close_btn.click()
        except:
            pass
        time.sleep(3)

        # [STEP 10] Real 'Get Link' button
        print("[STEP 10] Clicking 'Get Link'...")
        get_link_button = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Get Link')] | //*[contains(text(), 'GET LINK')] | //*[contains(@class, 'btn') and contains(text(), 'Link')]")))
        
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", get_link_button)
        time.sleep(3) 

        # First Click (Usually triggers pop-under ad)
        driver.execute_script("arguments[0].click();", get_link_button)
        time.sleep(3)

        # Second Click (Usually triggers the real link)
        try:
            driver.execute_script("arguments[0].click();", get_link_button)
        except:
            pass

        print("🎉 [FINAL SUCCESS] Script triggered the final destination link!")
        
        # --- SMART TAB HANDLING ---
        # Ab hum instantly tab band nahi karenge. Hum har khule hue tab mein ja kar dekhenge
        time.sleep(5)
        print(" -> Scanning all open tabs for destination URL...")
        for window in driver.window_handles:
            driver.switch_to.window(window)
            print(f" -> Active Tab URL: {driver.current_url}")
            
        print("Keeping the window alive for 25 seconds to register the view on Arolinks servers...")
        time.sleep(25)

    except Exception as e:
        print(f"❌ [ERROR] Processing workflow aborted: {e}")
        
    finally:
        driver.quit()

target_url = "https://arolinks.com/QfsX"
run_arolinks_fail_safe(target_url)