import asyncio
import random
from playwright.async_api import async_playwright

# ==========================================
# ⚙️ SCRIPT CONFIGURATION
# ==========================================
TOTAL_BOTS = 10                  # Pehle 10 bots test karein taaki 200MB jaldi khatam na ho
MAX_TEST_DURATION_MINUTES = 1  

TARGET_URL = "https://www.effectivecpmnetwork.com/ir6403tm?key=b4599e1b2bc92bc0e3b102e50f026c03" 

RANDOM_ORIGIN_SITES = [
    "https://duckduckgo.com",
    "https://www.bing.com",
    "https://en.wikipedia.org/wiki/Special:Random",
    "https://dev.to",
    "https://news.ycombinator.com/",
    "https://www.yahoo.com"
]

# ==========================================
# 🧠 HUMAN BEHAVIOR LOGIC
# ==========================================
async def human_scroll(page):
    scrolls = random.randint(2, 5)
    for _ in range(scrolls):
        scroll_amount = random.randint(300, 800)
        if random.random() > 0.8:
            scroll_amount = -300 
        await page.mouse.wheel(0, scroll_amount)
        await asyncio.sleep(random.uniform(1.5, 4.0))

async def human_behavior_on_target(page, bot_id):
    print(f"   [Bot {bot_id}] Target Site par pahonch gaya! Padh raha hai...")
    initial_wait = random.choice([10.0, 30.0, 60.0]) + random.uniform(1.0, 5.0)
    print(f"   [Bot {bot_id}] Page par {int(initial_wait)} seconds wait karega.")
    await asyncio.sleep(initial_wait)
    await human_scroll(page)
    
    try:
        links = await page.locator("a").all()
        if len(links) > 5:
            random_link = random.choice(links[2:10])
            print(f"   [Bot {bot_id}] Ek internal link par click kar raha hai...")
            await random_link.click(timeout=15000)
            await asyncio.sleep(random.uniform(5.0, 10.0))
            await human_scroll(page)
            
            print(f"   [Bot {bot_id}] Back button daba raha hai...")
            await page.go_back(timeout=15000)
            await asyncio.sleep(random.uniform(3.0, 6.0))
    except Exception as e:
        pass

# ==========================================
# 🚀 MAIN BOT RUNNER
# ==========================================
async def run_bot(bot_id):
    delay_seconds = random.uniform(0, MAX_TEST_DURATION_MINUTES * 60)
    print(f"⏳ Bot {bot_id}: {int(delay_seconds / 60)} min {int(delay_seconds % 60)} sec baad start hoga.")
    await asyncio.sleep(delay_seconds)
    
    print(f"🟢 Bot {bot_id}: Mission Shuru!")
    
    # ---------------------------------------------------
    # 🔒 NAYA PROXY LOGIC (With New 200MB Details)
    # ---------------------------------------------------
    random_sid = random.randint(10000000, 99999999)
    # Naya username aur password update kar diya gaya hai
    proxy_username = f"paCRkRTlf540_custom_zone_US_st__city_sid_{random_sid}_time_5"
    proxy_password = "5195429"
    proxy_server = "http://change4.owlproxy.com:7778"
    
    proxy_settings = {
        "server": proxy_server,
        "username": proxy_username,
        "password": proxy_password
    }
    
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(
                headless=False, 
                proxy=proxy_settings
            )
            context = await browser.new_context()
            page = await context.new_page()

            # --- STEP 1: Random Origins ---
            sites_to_visit = random.sample(RANDOM_ORIGIN_SITES, random.randint(1, 2))
            for site in sites_to_visit:
                print(f"   [Bot {bot_id}] Origin Site: {site} par ghum raha hai...")
                await page.goto(site, timeout=60000)
                await human_scroll(page)
                await asyncio.sleep(random.uniform(2.0, 5.0))

            # --- STEP 2: Target Website ---
            print(f"   [Bot {bot_id}] -> Target Website ({TARGET_URL}) par ja raha hai...")
            await page.goto(TARGET_URL, timeout=90000)
            
            # --- STEP 3: Human Behavior ---
            await human_behavior_on_target(page, bot_id)

            print(f"✅ Bot {bot_id}: Successfully Testing Complete!")

        except Exception as e:
            print(f"❌ Bot {bot_id} Error: {e}")
        
        finally:
            if 'browser' in locals():
                await browser.close()

async def main():
    print(f"--- Firing {TOTAL_BOTS} Bots with a maximum spread of {MAX_TEST_DURATION_MINUTES} minutes ---")
    tasks = []
    for i in range(1, TOTAL_BOTS + 1):
        tasks.append(run_bot(i))
    
    await asyncio.gather(*tasks)
    print("\n🎉 ALL BOTS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(main())