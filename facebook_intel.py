import asyncio
import json
import sys
import re
from datetime import datetime, timezone
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def get_facebook_intel(username):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        await Stealth().apply_stealth_async(page)
        
        url = f"https://www.facebook.com/{username}"
        print(f"[*] Reconnaissance started for Facebook Target: {url}")
        
        # Intercepted data
        intercepted_data = {"graphql": []}
        
        async def handle_response(response):
            try:
                r_url = response.url
                # Intercept GraphQL responses
                if "/api/graphql" in r_url and response.status == 200:
                    text = await response.text()
                    try:
                        parsed = json.loads(text)
                        intercepted_data["graphql"].append(parsed)
                    except:
                        # Sometimes multiple JSON objects concatenated
                        for line in text.strip().split('\n'):
                            try:
                                parsed = json.loads(line)
                                intercepted_data["graphql"].append(parsed)
                            except:
                                pass
            except:
                pass
        
        page.on("response", handle_response)
        
        try:
            print(f"[*] Navigating to {url}...")
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(8)
            
            # Scroll to load content
            print("[*] Deep Scrolling for intelligence gathering...")
            for _ in range(4):
                await page.mouse.wheel(0, 2000)
                await asyncio.sleep(2)
            
            # ============ EXTRACTION ============
            
            # Strategy 1: OpenGraph Meta Tags
            meta_data = {}
            try:
                meta_data = await page.evaluate('''() => {
                    const get = (name) => {
                        const el = document.querySelector(`meta[property="${name}"], meta[name="${name}"]`);
                        return el ? el.getAttribute("content") : null;
                    };
                    return {
                        title: document.title,
                        og_title: get("og:title"),
                        og_description: get("og:description"),
                        og_image: get("og:image"),
                        og_url: get("og:url"),
                        og_type: get("og:type"),
                        al_url: get("al:android:url"),
                        description: get("description")
                    };
                }''')
                print(f"[+] Extracted OG meta tags")
            except:
                pass
            
            # Strategy 2: Page content scraping
            dom_data = {}
            try:
                dom_data = await page.evaluate('''() => {
                    const getText = (sel) => {
                        const el = document.querySelector(sel);
                        return el ? el.textContent.trim() : null;
                    };
                    
                    // Profile name - try multiple selectors
                    const name = getText('h1') || getText('[data-testid="profile_name"]') || getText('.x1heor9g');
                    
                    // Bio/intro section
                    const bioItems = [];
                    document.querySelectorAll('[data-pagelet="ProfileTilesFeed_0"] span, .x1lliihq span').forEach(el => {
                        const text = el.textContent.trim();
                        if (text && text.length > 5 && text.length < 200) {
                            bioItems.push(text);
                        }
                    });
                    
                    // Profile picture
                    const profileImg = document.querySelector('[data-imgperflogname="profileCoverPhoto"] img, svg image, [role="img"] image')?.getAttribute('xlink:href') || 
                                       document.querySelector('.x1rg5ohu img[data-imgperflogname]')?.src;
                    
                    // Cover photo
                    const coverImg = document.querySelector('[data-imgperflogname="profileCoverPhoto"] img')?.src;
                    
                    // Visible posts
                    const posts = [];
                    document.querySelectorAll('[data-ad-preview="message"], [data-testid="post_message"] span').forEach(el => {
                        const text = el.textContent.trim();
                        if (text && text.length > 10) {
                            posts.push(text.substring(0, 300));
                        }
                    });
                    
                    // About section items (work, education, location)
                    const aboutItems = [];
                    document.querySelectorAll('[data-pagelet="ProfileTilesFeed_0"] li, .x9f619 span').forEach(el => {
                        const text = el.textContent.trim();
                        if (text && text.length > 3 && text.length < 200 && !text.includes('·')) {
                            aboutItems.push(text);
                        }
                    });
                    
                    // Follower/friend count
                    let followers = null;
                    let friends = null;
                    document.querySelectorAll('a[href*="friends"], a[href*="followers"], span').forEach(el => {
                        const text = el.textContent.trim();
                        const followerMatch = text.match(/([\d,.]+[KMB]?)\s*followers/i);
                        const friendMatch = text.match(/([\d,.]+[KMB]?)\s*friends/i);
                        if (followerMatch) followers = followerMatch[1];
                        if (friendMatch) friends = friendMatch[1];
                    });
                    
                    return {
                        name, bioItems: [...new Set(bioItems)].slice(0, 10),
                        profileImg, coverImg,
                        posts: [...new Set(posts)].slice(0, 10),
                        aboutItems: [...new Set(aboutItems)].slice(0, 15),
                        followers, friends
                    };
                }''')
                print(f"[+] Extracted DOM data")
            except Exception as e:
                print(f"[!] DOM extraction error: {e}")
            
            # Strategy 3: Extract from GraphQL intercepts
            graphql_profile = {}
            graphql_posts = []
            for packet in intercepted_data["graphql"]:
                try:
                    # Look for user profile data in GraphQL responses
                    def deep_find(obj, keys, depth=0):
                        if depth > 10: return None
                        if isinstance(obj, dict):
                            for k in keys:
                                if k in obj: return obj[k]
                            for v in obj.values():
                                r = deep_find(v, keys, depth + 1)
                                if r: return r
                        elif isinstance(obj, list):
                            for item in obj:
                                r = deep_find(item, keys, depth + 1)
                                if r: return r
                        return None
                    
                    user = deep_find(packet, ["user", "profile_owner"])
                    if user and isinstance(user, dict) and user.get("name"):
                        graphql_profile = user
                except:
                    pass
            
            # Parse Facebook ID from meta or URL
            fb_id = "N/A"
            al_url = meta_data.get("al_url", "")
            if al_url:
                id_match = re.search(r'/(\d+)', al_url)
                if id_match:
                    fb_id = id_match.group(1)
            
            # Parse intro items for work/education/location
            work = []
            education = []
            location = "N/A"
            for item in dom_data.get("aboutItems", []) + dom_data.get("bioItems", []):
                item_lower = item.lower()
                if any(kw in item_lower for kw in ["works at", "worked at", "ceo", "founder", "engineer", "manager"]):
                    work.append(item)
                elif any(kw in item_lower for kw in ["studied at", "went to", "university", "college", "school"]):
                    education.append(item)
                elif any(kw in item_lower for kw in ["lives in", "from ", "moved to"]):
                    location = item
            
            # Build Dossier
            dossier = {
                "dossier_meta": {
                    "target": f"fb/{username}",
                    "collection_time_utc": datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
                    "clearance_level": "TOP SECRET // Facebook Reconnaissance",
                    "graphql_packets_intercepted": len(intercepted_data["graphql"])
                },
                "account_archeology": {
                    "Full_Name": graphql_profile.get("name", dom_data.get("name", meta_data.get("og_title", "N/A"))),
                    "Facebook_ID": fb_id,
                    "Profile_URL": meta_data.get("og_url", url),
                    "Profile_Image": dom_data.get("profileImg", meta_data.get("og_image", "N/A")),
                    "Cover_Photo": dom_data.get("coverImg", "N/A"),
                    "Page_Type": meta_data.get("og_type", "N/A")
                },
                "public_metrics": {
                    "Followers": dom_data.get("followers", "N/A"),
                    "Friends": dom_data.get("friends", "N/A")
                },
                "about_intelligence": {
                    "Work": work if work else "N/A",
                    "Education": education if education else "N/A",
                    "Location": location,
                    "Bio_Items": dom_data.get("bioItems", [])[:10],
                    "Description": meta_data.get("og_description", meta_data.get("description", "N/A"))
                },
                "visible_posts": dom_data.get("posts", [])[:10],
                "graphql_intelligence": {
                    "Profile_Data_Captured": bool(graphql_profile),
                    "Username_from_GraphQL": graphql_profile.get("username", graphql_profile.get("vanity", "N/A")),
                    "Profile_Type": graphql_profile.get("__typename", "N/A")
                }
            }
            
            await browser.close()
            return dossier
        
        except Exception as e:
            print(f"[!] Intelligence Failure: {e}")
            await browser.close()
            return None

async def main():
    username = sys.argv[1] if len(sys.argv) > 1 else "zuck"
    print(f"[*] Initializing Facebook Dossier Generation for {username}...")
    
    dossier = await get_facebook_intel(username)
    
    if dossier:
        output = json.dumps(dossier, indent=2, ensure_ascii=False)
        try:
            print(output)
        except UnicodeEncodeError:
            print(output.encode('utf-8', errors='replace').decode('utf-8'))
        print("\n[+] Intelligence Dossier successfully compiled.")
    else:
        print("[!] Failed to compile Intelligence Dossier.")

if __name__ == "__main__":
    asyncio.run(main())
