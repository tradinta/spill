import asyncio
import json
import re
from datetime import datetime
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def get_tiktok_user_info(username):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Professional User-Agent
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        
        # Apply stealth to bypass bot detection
        stealth = Stealth()
        await stealth.apply_stealth_async(page)
        
        url = f"https://www.tiktok.com/@{username}"
        print(f"[*] Navigating to {url}...")
        
        try:
            # Go to the profile page
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # Wait for the rehydration script which contains all the data
            print("[*] Waiting for data script...")
            script_selector = 'script#__UNIVERSAL_DATA_FOR_REHYDRATION__'
            try:
                await page.wait_for_selector(script_selector, timeout=20000)
            except:
                print("[!] Script tag not found, trying fallback...")
            
            # Extract content of the script tag
            content = await page.evaluate(f'document.querySelector("{script_selector}").textContent')
            data = json.loads(content)
            
            # Navigate the nested JSON structure
            # Structure usually: __DEFAULT_SCOPE__ -> webapp.user-detail -> userInfo
            user_detail = data.get("__DEFAULT_SCOPE__", {}).get("webapp.user-detail", {})
            user_info = user_detail.get("userInfo", {})
            
            if not user_info:
                print("[!] Error: Could not find user info in script data.")
                return None
            
            user = user_info.get("user", {})
            stats = user_info.get("stats", {})
            
            # Helper to format numbers with commas
            def format_num(val):
                try:
                    return f"{int(val):,}"
                except:
                    return "0"

            # Format profile data
            nick_mod = user.get("nickNameModifyTime", user.get("nicknameModifyTime", 0))
            user_mod = user.get("uniqueIdModifyTime", 0)
            
            profile = {
                "Nickname": user.get("nickname", "N/A"),
                "Username": f"@{user.get('uniqueId', username)}",
                "Country": user.get("region", data.get("__DEFAULT_SCOPE__", {}).get("webapp.app-context", {}).get("region", "N/A")),
                "Language": user.get("language", "N/A"),
                "About": user.get("signature", "N/A"),
                "User ID": user.get("id", "N/A"),
                "SecUID": user.get("secUid", "N/A"),
                "Bio Link": user.get("bioLink", {}).get("link", "N/A") if user.get("bioLink") else "N/A",
                "Account Created": datetime.fromtimestamp(user.get("createTime", 0)).strftime('%Y-%m-%d %H:%M:%S') if user.get("createTime") else "N/A",
                "Nickname Last Modified": datetime.fromtimestamp(nick_mod).strftime('%Y-%m-%d %H:%M:%S') if nick_mod else "N/A",
                "Username Last Modified": datetime.fromtimestamp(user_mod).strftime('%Y-%m-%d %H:%M:%S') if user_mod else "N/A",
                "Avatar URL": user.get("avatarLarger", "N/A")
            }
            
            # Change "0" timestamp or similar to N/A
            if profile["Nickname Last Modified"] == "1970-01-01 00:00:00":
                profile["Nickname Last Modified"] = "N/A"
            if profile["Username Last Modified"] == "1970-01-01 00:00:00":
                profile["Username Last Modified"] = "N/A"
            
            # Format stats
            stats_formatted = {
                "Followers": format_num(stats.get("followerCount", 0)),
                "Following": format_num(stats.get("followingCount", 0)),
                "Hearts": format_num(stats.get("heartCount", 0)),
                "Videos": format_num(stats.get("videoCount", 0)),
                "Friends": format_num(stats.get("friendCount", 0))
            }
            
            # Helper for country names
            country_map = {
                "US": "United States",
                "KE": "Kenya",
                "UK": "United Kingdom",
                "GB": "United Kingdom",
                "CA": "Canada",
                "AU": "Australia",
                # Add more if needed, but these are common
            }
            iso_code = profile["Country"]
            profile["Country"] = country_map.get(iso_code, iso_code)

            result = {
                "profile": profile,
                "stats": stats_formatted
            }
            
            await browser.close()
            return result

        except Exception as e:
            print(f"[!] Critical error: {e}")
            await browser.close()
            return None

async def main():
    import sys
    username = sys.argv[1] if len(sys.argv) > 1 else "tonsic"
    max_retries = 3
    attempt = 0
    
    while attempt < max_retries:
        attempt += 1
        print(f"[*] Attempt {attempt} for user '{username}'...")
        info = await get_tiktok_user_info(username)
        
        if info:
            print("[+] Success!")
            print(json.dumps(info, indent=2))
            with open(f"tiktok_{username}_info.json", "w") as f:
                json.dump(info, f, indent=2)
            break
        else:
            print(f"[!] Attempt {attempt} failed.")
            if attempt < max_retries:
                wait_time = attempt * 5
                print(f"[*] Waiting {wait_time} seconds before retry...")
                await asyncio.sleep(wait_time)
            else:
                print("[!] Max retries reached. Tool failed to get all info.")

if __name__ == "__main__":
    asyncio.run(main())
