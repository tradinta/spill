import asyncio
import json
import sys
from datetime import datetime
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def get_tiktok_intel(username):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        await Stealth().apply_stealth_async(page)
        
        url = f"https://www.tiktok.com/@{username}"
        print(f"[*] Intelligence collection started for: {url}")
        
        # Data container for intercepted responses
        # Data container for intercepted responses
        intel_data = {"items": [], "followers": [], "commenters": []}
        
        async def handle_response(response):
            # Intercept item list (videos)
            if "item_list" in response.url and response.status == 200:
                try:
                    text = await response.text()
                    parsed = json.loads(text)
                    intel_data["items"].extend(parsed.get("itemList", []))
                except: pass
            
            # Intercept follower list
            if "follower/list" in response.url and response.status == 200:
                try:
                    text = await response.text()
                    parsed = json.loads(text)
                    intel_data["followers"].extend(parsed.get("followerList", []))
                except: pass
                
            # Intercept comments to get regional proxy for followers
            if "comment/list" in response.url and response.status == 200:
                try:
                    text = await response.text()
                    parsed = json.loads(text)
                    comments = parsed.get("comments", [])
                    for c in comments:
                        region = c.get("user", {}).get("region")
                        if region: intel_data["commenters"].append(region)
                except: pass

        page.on("response", handle_response)
        
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # Wait for data script or some network activity
            await asyncio.sleep(5)
            
            # Wait for data script
            script_selector = 'script#__UNIVERSAL_DATA_FOR_REHYDRATION__'
            await page.wait_for_selector(script_selector, state="attached", timeout=20000)
            
            content = await page.evaluate(f'document.querySelector("{script_selector}").textContent')
            data = json.loads(content)
            
            # 1. System DNA (App Context)
            app_context = data.get("__DEFAULT_SCOPE__", {}).get("webapp.app-context", {})
            
            # 2. Target Profile Data
            user_detail = data.get("__DEFAULT_SCOPE__", {}).get("webapp.user-detail", {})
            user_info = user_detail.get("userInfo", {})
            user = user_info.get("user", {})
            stats = user_info.get("stats", {})
            stats_v2 = user_info.get("statsV2", {})
            
            # 3. Content Portfolio (Combined from rehydration and interception)
            item_list = intel_data["items"] if intel_data["items"] else user_detail.get("itemList", [])
            if not item_list:
                # Some versions put it in default scope directly or nested differently
                item_list = data.get("__DEFAULT_SCOPE__", {}).get("webapp.item-list", {}).get("itemList", [])
            
            video_metrics = []
            sound_dna = {"commercial": 0, "original": 0}
            
            for item in item_list[:15]:  # Analyze top 15 videos
                v_stats = item.get("statsV2", item.get("stats", {}))
                music = item.get("music", {})
                
                def get_int(d, key):
                    val = d.get(key, 0)
                    try: return int(val)
                    except: return 0

                v_views = get_int(v_stats, "playCount")
                v_likes = get_int(v_stats, "diggCount")
                
                video_metrics.append({
                    "id": item.get("id"),
                    "views": v_views,
                    "likes": v_likes,
                    "shares": get_int(v_stats, "shareCount"),
                    "comments": get_int(v_stats, "commentCount"),
                    "is_commercial": music.get("commercial", False),
                    "video_hash": item.get("video", {}).get("id", "N/A"),
                    "cover_hash": item.get("video", {}).get("cover", "N/A").split("/")[-1].split("~")[0] if item.get("video", {}).get("cover") else "N/A"
                })
                if music.get("commercial"): sound_dna["commercial"] += 1
                else: sound_dna["original"] += 1

            # 4. Regional Proxy (Follower Geography)
            f_geo = {}
            # Combine direct followers and commenter regions
            all_regions = intel_data["commenters"] + [f.get("region") for f in intel_data["followers"] if f.get("region")]
            for r in all_regions:
                f_geo[r] = f_geo.get(r, 0) + 1
            
            top_regions = dict(sorted(f_geo.items(), key=lambda x: x[1], reverse=True)[:5])

            def format_ts(ts):
                if not ts or ts == 0: return "N/A"
                return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            def format_num(val):
                try: return f"{int(val):,}"
                except: return str(val)

            # Build Intelligence Dossier
            dossier = {
                "dossier_meta": {
                    "target": f"@{username}",
                    "collection_time_utc": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                    "clearance_level": "TOP SECRET // DEEP INTELLIGENCE"
                },
                "system_identity_dna": {
                    "OdinID": app_context.get("odinId", "HIDDEN"),
                    "WebID": app_context.get("webId", "HIDDEN"),
                    "WID": app_context.get("wid", "HIDDEN"),
                    "Session_Nonce": app_context.get("nonce", "HIDDEN"),
                    "Cluster_Region": app_context.get("clusterRegion", "N/A"),
                    "Storage_Node": f"DC_{app_context.get('clusterRegion', 'UNKNOWN').split('_')[-1]}",
                    "Bot_Classification": app_context.get("botType", "others")
                },
                "account_archeology": {
                    "User_Internal_ID": user.get("id", "N/A"),
                    "SecUID": user.get("secUid", "N/A"),
                    "Account_Created": format_ts(user.get("createTime")),
                    "Nickname_Last_Modified": format_ts(user.get("nickNameModifyTime")),
                    "Username_Last_Modified": format_ts(user.get("uniqueIdModifyTime")),
                    "Account_Age_Days": (datetime.utcnow() - datetime.fromtimestamp(user.get("createTime", 0))).days if user.get("createTime") else "N/A"
                },
                "social_graph_interconnects": {
                    "Instagram": user.get("insId", "N/A"),
                    "YouTube": user.get("youtubeId", "N/A"),
                    "Twitter": user.get("twitterId", "N/A"),
                    "Bio_Link": user.get("bioLink", {}).get("link", "N/A") if user.get("bioLink") else "N/A"
                },
                "behavioral_fingerprint": {
                    "Digital_Language": user.get("language", "N/A"),
                    "System_Region": app_context.get("region", "N/A"),
                    "Interface_Language": app_context.get("language", "N/A"),
                    "Bio_Signature": user.get("signature", "N/A"),
                    "Sound_Preference": "Commercial Bias" if sound_dna["commercial"] > sound_dna["original"] else "Original Bias",
                    "Regional_Engagement_Proxy": top_regions
                },
                "engagement_velocity_analysis": {
                    "Followers": format_num(stats_v2.get("followerCount", stats.get("followerCount", 0))),
                    "Recent_Portfolio_Velocity": f"{len(video_metrics)} items analyzed",
                    "Avg_Views_Per_Video": format_num(sum(v['views'] for v in video_metrics)/len(video_metrics)) if video_metrics else "0",
                    "Avg_Likes_Per_Video": format_num(sum(v['likes'] for v in video_metrics)/len(video_metrics)) if video_metrics else "0",
                    "Engagement_Ratio": f"{(int(stats.get('heartCount', 0)) / int(stats.get('followerCount', 1))):.2f}" if stats.get('followerCount') else "0.00"
                },
                "content_video_hashes": video_metrics[:10]  # Show top 10 hashes
            }
            
            await browser.close()
            return dossier

        except Exception as e:
            print(f"[!] Intelligence Failure: {e}")
            await browser.close()
            return None

async def main():
    username = sys.argv[1] if len(sys.argv) > 1 else "tonsic"
    print(f"[*] Initializing Dossier Generation for {username}...")
    
    dossier = await get_tiktok_intel(username)
    
    if dossier:
        print(json.dumps(dossier, indent=2))
        print("\n[+] Dossier successfully compiled.")
    else:
        print("[!] Failed to compile dossier.")

if __name__ == "__main__":
    asyncio.run(main())
