import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
import random

# Aapki Proxy ki details (Username me se sid hata diya h, wo hum niche auto-generate karenge)
PROXY_SERVER = "http://change4.owlproxy.com:7778"
BASE_USERNAME = "rloVBWLSZl30_custom_zone_US_st__city_sid_"
PROXY_PASS = "5194096"

async def run_ig_viewer(bot_id, reel_url):
    print(f"Bot {bot_id}: Mission Started...")
    
    try:
        async with async_playwright() as p:
            # MAGIC TRICK: Har bot ke liye random Session ID (sid) generate karna (Jaise: sid_12345678_time_5)
            # Isse OwlProxy har bot ko 100% naya IP dega!
            random_sid = random.randint(10000000, 99999999)
            dynamic_username = f"{BASE_USERNAME}{random_sid}_time_5"
            
            proxy_settings = {
                "server": PROXY_SERVER,
                "username": dynamic_username,
                "password": PROXY_PASS
            }
            
            print(f"Bot {bot_id} Username Setup: {dynamic_username}")
            
            # Browser open karna (headless=False rakha h dekhne ke liye)
            browser = await p.chromium.launch(
                headless=True, 
                proxy=proxy_settings
            )
            
            # Mobile jaisa setup
            context = await browser.new_context(
                viewport={'width': 390, 'height': 844},
                user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
            )
            page = await context.new_page()
            
            # Stealth script lagana
            await stealth_async(page)

            print(f"Bot {bot_id}: IP Check kar raha hu...")
            # IP Check karne ke liye ek test site pehle open karte hain
            await page.goto("https://api.ipify.org", timeout=60000)
            assigned_ip = await page.inner_text("body")
            print(f"✅ Bot {bot_id} Got New IP: {assigned_ip}")

            print(f"Bot {bot_id}: Opening Instagram Reel...")
            await page.goto(reel_url, timeout=90000)

            print(f"Bot {bot_id}: Loading video...")
            await asyncio.sleep(random.uniform(4.0, 7.0))
            
            await page.mouse.wheel(0, random.randint(200, 600))
            
            watch_time = random.uniform(30.0, 35.0)
            print(f"Bot {bot_id}: Watching Reel for {int(watch_time)} seconds...")
            await asyncio.sleep(watch_time)

            print(f"✅ Bot {bot_id}: View Successful! Closing browser.")
            await browser.close()
            
    except Exception as e:
        print(f"❌ Bot {bot_id} Failed: {e}")

async def main():
    # ⚠️ Yahan apni Reel ka link zaroor daalein
    REEL_URL = "https://www.instagram.com/th3_og_gam3r/reel/DbVIbpbpmM4/?hl=en"
    
    TOTAL_BOTS = 62 # Abhi 2 bots test karein
    
    tasks = []
    for i in range(TOTAL_BOTS):
        task = run_ig_viewer(bot_id=i+1, reel_url=REEL_URL)
        tasks.append(task)
        await asyncio.sleep(2)

    print(f"--- Firing {TOTAL_BOTS} Bots ---")
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())