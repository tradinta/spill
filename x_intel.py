import asyncio
import json
import sys
import re
from datetime import datetime, timezone
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def get_x_intel(username):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Use a high-quality user agent
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        await Stealth().apply_stealth_async(page)
        
        url = f"https://x.com/{username}"
        print(f"[*] Reconnaissance started for X Target: {url}")
        
        # Data container for intercepted GraphQL responses
        intel_data = {"profile": None, "timeline": [], "lists": [], "headers": {}}
        
        # Intercept network responses to find GraphQL user data
        async def handle_response(response):
            try:
                r_url = response.url
                # Intercept profile data
                if "UserByScreenName" in r_url and response.status == 200:
                    text = await response.text()
                    intel_data["profile"] = json.loads(text)
                    print(f"[+] Intercepted X Profile GraphQL Packet")
                
                # Intercept timeline (Tweets, Replies, etc.)
                timeline_patterns = ["UserTweets", "UserTweetsAndReplies", "ProfileTimeline", "UserMedia", "TweetDetail"]
                if any(p in r_url for p in timeline_patterns):
                    print(f"[*] Match Potential Timeline: {r_url.split('/')[-1].split('?')[0]} Status: {response.status}")
                    if response.status == 200:
                        text = await response.text()
                        parsed = json.loads(text)
                        
                        # Deep Debug: Inspect structure
                        def find_instructions(obj, depth=0):
                            if depth > 8: return None
                            if isinstance(obj, dict):
                                if "instructions" in obj: return obj["instructions"]
                                for k, v in obj.items():
                                    res = find_instructions(v, depth + 1)
                                    if res: return res
                            elif isinstance(obj, list):
                                for item in obj:
                                    res = find_instructions(item, depth + 1)
                                    if res: return res
                            return None

                        instructions = find_instructions(parsed.get("data", {}))
                        if not instructions:
                            instructions = find_instructions(parsed)
                        
                        if instructions:
                            count_before = len(intel_data["timeline"])
                            for instr in instructions:
                                if instr.get("type") in ["TimelineAddEntries", "TimelinePinEntry"]:
                                    entries = instr.get("entries", [])
                                    if "entry" in instr: entries.append(instr["entry"])
                                    intel_data["timeline"].extend(entries)
                            # print(f"[+] Intercepted X Timeline (Added {len(intel_data['timeline']) - count_before} entries)")
                        # else:
                        #    print(f"[!] Failed to find instructions in {r_url.split('/')[-1].split('?')[0]}")

                # Intercept User Lists
                if ("UserLists" in r_url or "OwnedLists" in r_url or "CombinedLists" in r_url) and response.status == 200:
                    text = await response.text()
                    parsed = json.loads(text)
                    # Support multiple list structures
                    lists_instr = parsed.get("data", {}).get("user", {}).get("result", {}).get("list_ownership_timeline", {}).get("timeline", {}).get("instructions", [])
                    if not lists_instr:
                        # Recursive search for instructions in lists
                        lists_instr = find_instructions(parsed.get("data", {}))
                        
                    if lists_instr:
                        for instr in lists_instr:
                            if instr.get("type") == "TimelineAddEntries":
                                for entry in instr.get("entries", []):
                                    list_data = entry.get("content", {}).get("itemContent", {}).get("list_results", {}).get("result", {})
                                    if list_data:
                                        intel_data["lists"].append({
                                            "name": list_data.get("name"),
                                            "description": list_data.get("description"),
                                            "member_count": list_data.get("member_count"),
                                            "subscriber_count": list_data.get("subscriber_count")
                                        })
                    # print(f"[+] Intercepted X User Lists ({len(intel_data['lists'])} lists)")

                # Capture technical DNA (headers)
                if "graphql" in r_url:
                    headers = await response.request.all_headers()
                    if not intel_data["headers"]:
                        intel_data["headers"] = {
                            "Guest_Token": headers.get("x-guest-token", "N/A"),
                            "Auth_Bearer": headers.get("authorization", "N/A")[:20] + "...",
                            "Client_Transaction_ID": headers.get("x-client-transaction-id", "N/A")
                        }
            except Exception as e:
                # print(f"[!] Intercept Error: {e}")
                pass

        page.on("response", handle_response)
        
        try:
            # Navigate to the target profile
            print(f"[*] Navigating to {url}...")
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # Wait for content to stabilize
            await asyncio.sleep(10)
            
            # Scroll more to trigger timeline and potential other data
            print("[*] Deep Scrolling for intelligence gathering...")
            for _ in range(8):
                await page.mouse.wheel(0, 1500)
                await asyncio.sleep(3)
            
            # Optional: Navigate to lists to trigger UserLists GraphQL
            print(f"[*] Probing for List Intelligence at {url}/lists...")
            await page.goto(f"{url}/lists", wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(5)
            
            if not intel_data["profile"]:
                print("[!] Diagnostic: No Profile GraphQL Intercepted.")
                await browser.close()
                return None

            # 1. Extract Data from GraphQL Packet
            user_result = intel_data["profile"].get("data", {}).get("user", {}).get("result", {})
            core = user_result.get("core", {})
            legacy = user_result.get("legacy", {})
            
            # 2. Behavioral Intelligence Analysis (Timeline)
            sources = {}
            timestamps = [] # List of (hour, weekday) tuples
            interactions = {} # Who they reply to
            retweeted_users = {} # Who they retweet
            mentions = {} # Users mentioned in text
            media_archive = []
            
            for entry in intel_data["timeline"]:
                content = entry.get("content", {}).get("itemContent", {}).get("tweet_results", {}).get("result", {})
                if not content: continue
                
                # Handle potential "TweetWithVisibilityResults" wrapper
                if "tweet" in content: content = content["tweet"]
                
                tweet_legacy = content.get("legacy", {})
                
                # Media Extraction
                extended_entities = tweet_legacy.get("extended_entities", {})
                for media in extended_entities.get("media", []):
                    media_url = media.get("media_url_https")
                    if media_url:
                        media_archive.append({
                            "type": media.get("type"),
                            "url": media_url,
                            "tweet_id": tweet_legacy.get("id_str")
                        })

                # Source Fingerprint
                source = tweet_legacy.get("source", content.get("source", ""))
                if source:
                    clean_source = re.sub('<[^<]+?>', '', source)
                    sources[clean_source] = sources.get(clean_source, 0) + 1
                
                # Temporal Analysis (Sleep Cycle)
                created_at = tweet_legacy.get("created_at")
                if created_at:
                    dt = datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
                    timestamps.append((dt.hour, dt.weekday()))
                
                # Interaction Network
                # A. Direct Replies
                reply_to = tweet_legacy.get("in_reply_to_screen_name")
                if reply_to:
                    interactions[reply_to] = interactions.get(reply_to, 0) + 1
                
                # B. Retweets
                retweet_result = content.get("retweeted_status_result", {}).get("result", {})
                if retweet_result:
                    rt_user = retweet_result.get("core", {}).get("user_results", {}).get("result", {}).get("legacy", {}).get("screen_name")
                    if rt_user:
                        retweeted_users[rt_user] = retweeted_users.get(rt_user, 0) + 1
                
                # C. Mentions Extraction from Text
                full_text = tweet_legacy.get("full_text", "")
                found_mentions = re.findall(r'@(\w+)', full_text)
                for m in found_mentions:
                    if m.lower() != username.lower():
                        mentions[m] = mentions.get(m, 0) + 1

            # Generate Sleep Cycle Heatmap (Hour vs Day)
            # Days: 0=Mon, 6=Sun
            heatmap = {d: {h: 0 for h in range(24)} for d in range(7)}
            for hour, day in timestamps:
                heatmap[day][hour] += 1

            def format_num(val):
                try: return f"{int(val):,}"
                except: return str(val)

            # Build Intelligence Dossier
            dossier = {
                "dossier_meta": {
                    "target": f"@{username}",
                    "collection_time_utc": datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
                    "clearance_level": "TOP SECRET // X Reconnaissance"
                },
                "technical_dna": {
                    "Rest_ID": user_result.get("rest_id", "N/A"),
                    "Guest_Token": intel_data["headers"].get("Guest_Token"),
                    "Transaction_ID": intel_data["headers"].get("Client_Transaction_ID")
                },
                "account_archeology": {
                    "Account_Created": core.get("created_at", legacy.get("created_at", "N/A")),
                    "User_Name": core.get("name", legacy.get("name", "N/A")),
                    "Verified_Type": "Blue/Premium" if user_result.get("is_blue_verified") else "Standard",
                    "Location": legacy.get("location", "N/A"),
                    "Description": legacy.get("description", "N/A")
                },
                "behavioral_intelligence": {
                    "Device_Fingerprint": dict(sorted(sources.items(), key=lambda x: x[1], reverse=True)[:3]),
                    "Interaction_Network": {
                        "Top_Replies": dict(sorted(interactions.items(), key=lambda x: x[1], reverse=True)[:5]),
                        "Top_Retweets": dict(sorted(retweeted_users.items(), key=lambda x: x[1], reverse=True)[:5]),
                        "Top_Mentions": dict(sorted(mentions.items(), key=lambda x: x[1], reverse=True)[:5])
                    },
                    "Sleep_Cycle_Heatmap_UTC": heatmap,
                    "Peak_Activity_Hour_UTC": max(set([t[0] for t in timestamps]), key=[t[0] for t in timestamps].count) if timestamps else "N/A"
                },
                "visibility_diagnostics": {
                    "Search_Slop_Flag": user_result.get("search_slop", "N/A"),
                    "Is_Suspended": user_result.get("is_suspended", "FALSE"),
                    "Possible_Shadowban": "Detected" if user_result.get("can_media_tag") == False and legacy.get("screen_name") else "None Detected",
                    "Professional_Account": user_result.get("is_professional", "FALSE"),
                    "Flags": user_result.get("business_account_status", "Standard")
                },
                "public_metrics": {
                    "Followers": format_num(legacy.get("followers_count", 0)),
                    "Following": format_num(legacy.get("friends_count", 0)),
                    "Tweets_Total": format_num(legacy.get("statuses_count", 0)),
                    "Media_Archived_Count": format_num(legacy.get("media_count", 0)),
                    "Favorites_Count": format_num(legacy.get("favourites_count", 0))
                },
                "lists_intelligence": intel_data["lists"],
                "media_archive": media_archive[:20] # Limit to top 20 for the dossier
            }
            
            await browser.close()
            return dossier

        except Exception as e:
            print(f"[!] Intelligence Failure: {e}")
            await browser.close()
            return None

async def main():
    username = sys.argv[1] if len(sys.argv) > 1 else "elonmusk"
    print(f"[*] Initializing X Dossier Generation for {username}...")
    
    dossier = await get_x_intel(username)
    
    if dossier:
        print(json.dumps(dossier, indent=2))
        print("\n[+] Intelligence Dossier successfully compiled.")
    else:
        print("[!] Failed to compile Intelligence Dossier.")

if __name__ == "__main__":
    asyncio.run(main())
