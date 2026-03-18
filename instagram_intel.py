import asyncio
import json
import sys
import re
from datetime import datetime, timezone
from collections import Counter
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def get_instagram_intel(username):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        await Stealth().apply_stealth_async(page)
        
        url = f"https://www.instagram.com/{username}/"
        print(f"[*] Reconnaissance started for Instagram Target: {url}")
        
        # Data container
        intel_data = {"profile": None, "posts": [], "reels": []}
        
        async def handle_response(response):
            try:
                r_url = response.url
                
                # Intercept GraphQL profile/post data
                if "/graphql/query" in r_url and response.status == 200:
                    text = await response.text()
                    parsed = json.loads(text)
                    data = parsed.get("data", {})
                    
                    # Profile data via user query
                    user = data.get("user", {})
                    if user and user.get("edge_owner_to_timeline_media"):
                        intel_data["profile"] = user
                        edges = user.get("edge_owner_to_timeline_media", {}).get("edges", [])
                        intel_data["posts"].extend(edges)
                        print(f"[+] Intercepted Instagram GraphQL Profile ({len(edges)} posts)")
                    
                    # XDT user data (newer API)
                    xdt_user = data.get("xdt_api__v1__users__web_profile_info", {}).get("user", {})
                    if xdt_user:
                        intel_data["profile"] = xdt_user
                        print(f"[+] Intercepted Instagram XDT Profile Packet")
                    
                    # Timeline media edges
                    media = data.get("xdt_api__v1__feed__user_timeline_graphql_connection", {})
                    if media:
                        edges = media.get("edges", [])
                        intel_data["posts"].extend(edges)
                        print(f"[+] Intercepted Instagram Timeline ({len(edges)} posts)")

                # Intercept the web profile info API
                if "/api/v1/users/web_profile_info" in r_url and response.status == 200:
                    text = await response.text()
                    parsed = json.loads(text)
                    user = parsed.get("data", {}).get("user", {})
                    if user:
                        intel_data["profile"] = user
                        print(f"[+] Intercepted Instagram Web Profile API")

            except Exception as e:
                pass
        
        page.on("response", handle_response)
        
        try:
            print(f"[*] Navigating to {url}...")
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(8)
            
            # Scroll to trigger more post loading
            print("[*] Deep Scrolling for intelligence gathering...")
            for _ in range(6):
                await page.mouse.wheel(0, 2000)
                await asyncio.sleep(3)
            
            # Try to extract from page meta tags and LD+JSON as fallback
            profile_from_meta = {}
            try:
                ld_json = await page.evaluate('''() => {
                    const scripts = document.querySelectorAll('script[type="application/ld+json"]');
                    for (const s of scripts) {
                        try {
                            const d = JSON.parse(s.textContent);
                            if (d["@type"] === "ProfilePage" || d.mainEntity) return d;
                        } catch(e) {}
                    }
                    return null;
                }''')
                if ld_json:
                    main = ld_json.get("mainEntity", ld_json)
                    profile_from_meta = {
                        "name": main.get("name", ""),
                        "alternateName": main.get("alternateName", ""),
                        "description": main.get("description", ""),
                        "url": main.get("url", ""),
                        "followers": main.get("interactionStatistic", [{}])[0].get("userInteractionCount", 0) if main.get("interactionStatistic") else 0
                    }
                    print(f"[+] Extracted LD+JSON metadata")
            except:
                pass
            
            # Try extracting from shared data script
            shared_data = {}
            try:
                shared_data = await page.evaluate('''() => {
                    if (window._sharedData) return window._sharedData;
                    const scripts = document.querySelectorAll('script');
                    for (const s of scripts) {
                        if (s.textContent.includes('window._sharedData')) {
                            const match = s.textContent.match(/window\\._sharedData\\s*=\\s*(\\{.+?\\});/);
                            if (match) return JSON.parse(match[1]);
                        }
                    }
                    return {};
                }''')
                if shared_data:
                    entry = shared_data.get("entry_data", {}).get("ProfilePage", [{}])[0].get("graphql", {}).get("user", {})
                    if entry and entry.get("username"):
                        intel_data["profile"] = entry
                        edges = entry.get("edge_owner_to_timeline_media", {}).get("edges", [])
                        intel_data["posts"].extend(edges)
                        print(f"[+] Extracted SharedData profile ({len(edges)} posts)")
            except:
                pass
            
            # Build profile from whatever we have
            profile = intel_data.get("profile", {})
            
            if not profile and not profile_from_meta:
                print("[!] Diagnostic: No Profile Data Intercepted.")
                # Try one more fallback: scrape visible page elements
                try:
                    meta_desc = await page.evaluate('() => document.querySelector("meta[name=\\"description\\"]")?.content || ""')
                    title = await page.evaluate('() => document.title')
                    profile_from_meta["page_title"] = title
                    profile_from_meta["meta_description"] = meta_desc
                    # Parse followers from meta description
                    follower_match = re.search(r'([\d,.]+[KMB]?)\s*Followers', meta_desc)
                    following_match = re.search(r'([\d,.]+[KMB]?)\s*Following', meta_desc)
                    posts_match = re.search(r'([\d,.]+[KMB]?)\s*Posts', meta_desc)
                    if follower_match:
                        profile_from_meta["followers_text"] = follower_match.group(1)
                    if following_match:
                        profile_from_meta["following_text"] = following_match.group(1)
                    if posts_match:
                        profile_from_meta["posts_text"] = posts_match.group(1)
                    print(f"[+] Scraped meta tag fallback data")
                except:
                    pass
            
            # ============ ANALYSIS ============
            
            # Extract metrics from profile (handle both old and new API shapes)
            def safe_count(obj, key, alt_key=None):
                if isinstance(obj, dict):
                    val = obj.get(key, {})
                    if isinstance(val, dict):
                        return val.get("count", 0)
                    if alt_key:
                        return obj.get(alt_key, 0)
                    return val if isinstance(val, int) else 0
                return 0
            
            followers = safe_count(profile, "edge_followed_by", "follower_count")
            following = safe_count(profile, "edge_follow", "following_count")
            media_count = safe_count(profile, "edge_owner_to_timeline_media", "media_count")
            
            # Post Analysis
            timestamps = []
            hashtag_counts = Counter()
            locations = []
            mentioned_users = Counter()
            media_archive = []
            captions_all = []
            engagement_data = []
            
            for edge in intel_data["posts"]:
                node = edge.get("node", edge)
                
                # Timestamp
                taken_at = node.get("taken_at_timestamp", node.get("taken_at"))
                if taken_at:
                    dt = datetime.fromtimestamp(taken_at, tz=timezone.utc)
                    timestamps.append((dt.hour, dt.weekday()))
                
                # Caption analysis
                caption_edges = node.get("edge_media_to_caption", {}).get("edges", [])
                caption_text = ""
                if caption_edges:
                    caption_text = caption_edges[0].get("node", {}).get("text", "")
                elif node.get("caption"):
                    if isinstance(node["caption"], dict):
                        caption_text = node["caption"].get("text", "")
                    else:
                        caption_text = str(node["caption"])
                
                if caption_text:
                    captions_all.append(caption_text)
                    # Hashtags
                    tags = re.findall(r'#(\w+)', caption_text)
                    hashtag_counts.update(tags)
                    # Mentions
                    mentions = re.findall(r'@(\w+)', caption_text)
                    mentioned_users.update(mentions)
                
                # Location
                loc = node.get("location")
                if loc:
                    locations.append(loc.get("name", "Unknown"))
                
                # Media URLs
                display_url = node.get("display_url", node.get("image_versions2", {}).get("candidates", [{}])[0].get("url", ""))
                if display_url:
                    media_archive.append({
                        "type": "video" if node.get("is_video") or node.get("media_type") == 2 else "photo",
                        "url": display_url.split("?")[0] if "?" in display_url else display_url,
                        "id": node.get("id", node.get("pk", "N/A"))
                    })
                
                # Engagement
                likes = node.get("edge_liked_by", {}).get("count", node.get("like_count", 0))
                comments = node.get("edge_media_to_comment", {}).get("count", node.get("comment_count", 0))
                engagement_data.append({"likes": likes, "comments": comments})
            
            # Sleep Cycle Heatmap
            heatmap = {d: {h: 0 for h in range(24)} for d in range(7)}
            for hour, day in timestamps:
                heatmap[day][hour] += 1
            
            peak_hour = max(set([t[0] for t in timestamps]), key=[t[0] for t in timestamps].count) if timestamps else "N/A"
            
            # Location frequency
            location_freq = dict(Counter(locations).most_common(10))
            
            def format_num(val):
                try: return f"{int(val):,}"
                except: return str(val)
            
            # Avg engagement
            avg_likes = round(sum(e["likes"] for e in engagement_data) / len(engagement_data)) if engagement_data else 0
            avg_comments = round(sum(e["comments"] for e in engagement_data) / len(engagement_data)) if engagement_data else 0
            
            # Build Dossier
            dossier = {
                "dossier_meta": {
                    "target": f"@{username}",
                    "collection_time_utc": datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
                    "clearance_level": "TOP SECRET // Instagram Reconnaissance",
                    "posts_analyzed": len(intel_data["posts"])
                },
                "account_archeology": {
                    "Full_Name": profile.get("full_name", profile_from_meta.get("name", "N/A")),
                    "Username": profile.get("username", username),
                    "Biography": profile.get("biography", profile.get("bio", profile_from_meta.get("description", "N/A"))),
                    "External_URL": profile.get("external_url", profile.get("bio_links", [{}])[0].get("url", "N/A") if profile.get("bio_links") else "N/A"),
                    "Is_Verified": profile.get("is_verified", False),
                    "Is_Business": profile.get("is_business_account", profile.get("is_professional_account", False)),
                    "Business_Category": profile.get("category_name", profile.get("category", "N/A")),
                    "Is_Private": profile.get("is_private", False),
                    "Profile_Pic_URL": (profile.get("profile_pic_url_hd", profile.get("hd_profile_pic_url_info", {}).get("url", "")) or "").split("?")[0]
                },
                "public_metrics": {
                    "Followers": format_num(followers) if followers else profile_from_meta.get("followers_text", "N/A"),
                    "Following": format_num(following) if following else profile_from_meta.get("following_text", "N/A"),
                    "Total_Posts": format_num(media_count) if media_count else profile_from_meta.get("posts_text", "N/A"),
                    "Avg_Likes_Per_Post": format_num(avg_likes),
                    "Avg_Comments_Per_Post": format_num(avg_comments),
                    "Engagement_Rate": f"{((avg_likes + avg_comments) / followers * 100):.2f}%" if followers and (avg_likes + avg_comments) > 0 else "N/A"
                },
                "behavioral_intelligence": {
                    "Sleep_Cycle_Heatmap_UTC": heatmap,
                    "Peak_Activity_Hour_UTC": peak_hour,
                    "Top_Hashtags": dict(hashtag_counts.most_common(15)),
                    "Top_Mentioned_Users": dict(mentioned_users.most_common(10)),
                    "Frequent_Locations": location_freq
                },
                "media_archive": media_archive[:20]
            }
            
            await browser.close()
            return dossier

        except Exception as e:
            print(f"[!] Intelligence Failure: {e}")
            await browser.close()
            return None

async def main():
    username = sys.argv[1] if len(sys.argv) > 1 else "instagram"
    print(f"[*] Initializing Instagram Dossier Generation for @{username}...")
    
    dossier = await get_instagram_intel(username)
    
    if dossier:
        print(json.dumps(dossier, indent=2, ensure_ascii=False))
        print("\n[+] Intelligence Dossier successfully compiled.")
    else:
        print("[!] Failed to compile Intelligence Dossier.")

if __name__ == "__main__":
    asyncio.run(main())
