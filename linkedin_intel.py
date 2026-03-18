import asyncio
import json
import sys
import re
import httpx
from datetime import datetime, timezone
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

async def search_fallback(username):
    """Use search engines to extract LinkedIn profile snippets when auth wall blocks direct access."""
    print(f"[*] Attempting search engine fallback for LinkedIn/{username}...")
    profile_data = {}
    
    async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True, timeout=15) as client:
        # Try DuckDuckGo (less restrictive)
        try:
            resp = await client.get(f"https://duckduckgo.com/html/?q=site:linkedin.com/in/{username}")
            if resp.status_code == 200:
                text = resp.text
                # Extract snippet from search results
                snippets = re.findall(r'<a class="result__snippet"[^>]*>(.*?)</a>', text, re.DOTALL)
                titles = re.findall(r'<a class="result__a"[^>]*>(.*?)</a>', text, re.DOTALL)
                
                for title in titles:
                    clean = re.sub('<[^>]+>', '', title).strip()
                    if username.lower() in clean.lower() or "linkedin" in clean.lower():
                        # Parse name and headline from title like "Bill Gates - Co-chair | LinkedIn"
                        parts = clean.replace(" | LinkedIn", "").replace(" - LinkedIn", "").split(" - ", 1)
                        if len(parts) >= 1:
                            profile_data["name"] = parts[0].strip()
                        if len(parts) >= 2:
                            profile_data["headline"] = parts[1].strip()
                        break
                
                for snippet in snippets:
                    clean = re.sub('<[^>]+>', '', snippet).strip()
                    if clean and len(clean) > 20:
                        profile_data["description"] = clean[:500]
                        # Try to parse experience/location from snippet
                        exp_match = re.search(r'(?:Experience|Current):\s*(.+?)(?:\.|·|$)', clean)
                        loc_match = re.search(r'(?:Location|Based in):\s*(.+?)(?:\.|·|$)', clean)
                        edu_match = re.search(r'(?:Education):\s*(.+?)(?:\.|·|$)', clean)
                        if exp_match: profile_data["experience"] = exp_match.group(1).strip()
                        if loc_match: profile_data["location"] = loc_match.group(1).strip()
                        if edu_match: profile_data["education"] = edu_match.group(1).strip()
                        break
                
                if profile_data:
                    print(f"[+] Search engine fallback successful")
        except Exception as e:
            print(f"[!] Search fallback error: {e}")
    
    return profile_data


async def get_linkedin_intel(username):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        await Stealth().apply_stealth_async(page)
        
        url = f"https://www.linkedin.com/in/{username}/"
        print(f"[*] Reconnaissance started for LinkedIn Target: {url}")
        
        # Data containers
        intercepted_data = {"voyager": []}
        
        # Intercept Voyager API calls (LinkedIn's internal API)
        async def handle_response(response):
            try:
                r_url = response.url
                if "/voyager/api/" in r_url and response.status == 200:
                    ct = response.headers.get("content-type", "")
                    if "json" in ct:
                        text = await response.text()
                        parsed = json.loads(text)
                        intercepted_data["voyager"].append({
                            "url": r_url.split("?")[0],
                            "data": parsed
                        })
            except:
                pass
        
        page.on("response", handle_response)
        
        try:
            print(f"[*] Navigating to {url}...")
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(5)
            
            # Check if auth wall was hit
            current_url = page.url
            page_title = await page.title()
            h1_text = await page.evaluate('() => document.querySelector("h1")?.textContent?.trim() || ""')
            is_auth_walled = (
                "login" in current_url.lower() or 
                "signup" in current_url.lower() or 
                "authwall" in current_url.lower() or 
                "may be private" in page_title.lower() or
                "may be private" in h1_text.lower()
            )
            
            if is_auth_walled:
                print("[!] Auth wall detected. Trying public profile endpoint...")
                await page.goto(f"https://www.linkedin.com/in/{username}/?trk=public_profile", wait_until="domcontentloaded", timeout=30000)
                await asyncio.sleep(5)
                
                current_url = page.url
                h1_retry = await page.evaluate('() => document.querySelector("h1")?.textContent?.trim() || ""')
                still_walled = (
                    "login" in current_url.lower() or 
                    "authwall" in current_url.lower() or
                    "may be private" in h1_retry.lower()
                )
                if still_walled:
                    print("[!] Auth wall still active. Falling back to search engine extraction...")
                    search_data = await search_fallback(username)
                    # Build dossier from search results (or empty if nothing found)
                    await browser.close()
                    return {
                        "dossier_meta": {
                            "target": f"linkedin.com/in/{username}",
                            "collection_time_utc": datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
                            "clearance_level": "TOP SECRET // LinkedIn Reconnaissance",
                            "note": "Auth wall detected — data sourced from search engine snippets" if search_data else "Auth wall detected — limited data available without login"
                        },
                        "account_archeology": {
                            "Full_Name": search_data.get("name", "N/A"),
                            "Headline": search_data.get("headline", "N/A"),
                            "Location": search_data.get("location", "N/A"),
                            "Profile_URL": f"https://www.linkedin.com/in/{username}/",
                            "Profile_Image": "N/A (Auth Wall)",
                            "Connections": "N/A (Auth Wall)"
                        },
                        "professional_intelligence": {
                            "Experience": search_data.get("experience", "N/A"),
                            "Education": search_data.get("education", "N/A"),
                            "Skills": "N/A (Auth Wall)"
                        },
                        "meta_description_raw": search_data.get("description", "N/A")
                    }
            
            # Scroll to load more sections
            print("[*] Deep Scrolling for data loading...")
            for _ in range(5):
                await page.mouse.wheel(0, 2000)
                await asyncio.sleep(2)
            
            # ============ EXTRACTION STRATEGIES ============
            
            # Strategy 1: LD+JSON (Most reliable for public profiles)
            ld_json_data = {}
            try:
                ld_json_data = await page.evaluate('''() => {
                    const scripts = document.querySelectorAll('script[type="application/ld+json"]');
                    for (const s of scripts) {
                        try {
                            const d = JSON.parse(s.textContent);
                            if (d["@type"] === "Person" || d["@type"] === "ProfilePage") return d;
                        } catch(e) {}
                    }
                    return {};
                }''')
                if ld_json_data:
                    print(f"[+] Extracted LD+JSON Person schema")
            except:
                pass
            
            # Strategy 2: Meta Tags (OG + Twitter cards)
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
                        twitter_title: get("twitter:title"),
                        twitter_description: get("twitter:description"),
                        description: get("description")
                    };
                }''')
                print(f"[+] Extracted meta tags")
            except:
                pass
            
            # Strategy 3: DOM Scraping for visible sections
            dom_data = {}
            try:
                dom_data = await page.evaluate('''() => {
                    const getText = (sel) => {
                        const el = document.querySelector(sel);
                        return el ? el.textContent.trim() : null;
                    };
                    const getAll = (sel) => {
                        return Array.from(document.querySelectorAll(sel)).map(e => e.textContent.trim()).filter(t => t);
                    };
                    
                    // Profile header
                    const name = getText('h1') || getText('.top-card-layout__title');
                    const headline = getText('.top-card-layout__headline, .text-body-medium');
                    const location = getText('.top-card-layout__first-subline, .text-body-small:not(.inline)');
                    
                    // About section
                    const about = getText('.core-section-container__content p, [data-section="summary"] p, section.summary .core-section-container__content');
                    
                    // Experience items
                    const expItems = [];
                    document.querySelectorAll('.experience-item, .experience-group, li.profile-section-card').forEach(el => {
                        const title = el.querySelector('.experience-item__title, .profile-section-card__title, h3')?.textContent?.trim();
                        const subtitle = el.querySelector('.experience-item__subtitle, .profile-section-card__subtitle, h4')?.textContent?.trim();
                        const meta = el.querySelector('.experience-item__meta-item, .profile-section-card__meta, .date-range')?.textContent?.trim();
                        const desc = el.querySelector('.experience-item__description, p')?.textContent?.trim();
                        if (title || subtitle) {
                            expItems.push({title, company: subtitle, duration: meta, description: desc ? desc.substring(0, 200) : null});
                        }
                    });
                    
                    // Education items
                    const eduItems = [];
                    document.querySelectorAll('.education__list-item, section.education li').forEach(el => {
                        const school = el.querySelector('h3, .education__item--school')?.textContent?.trim();
                        const degree = el.querySelector('h4, .education__item--degree-info')?.textContent?.trim();
                        const dates = el.querySelector('.education__item--duration, .date-range')?.textContent?.trim();
                        if (school) {
                            eduItems.push({school, degree, dates});
                        }
                    });
                    
                    // Skills
                    const skills = getAll('.skill-categories-card__skill-item, .skills-section li, .skill-card-square__skill-name');
                    
                    // Connection count from page
                    const connectionsEl = document.querySelector('.top-card__subline-item--break, .connections');
                    const connections = connectionsEl ? connectionsEl.textContent.trim() : null;
                    
                    // Profile image
                    const profileImg = document.querySelector('.top-card-layout__entity-image, .profile-photo-edit__preview, img.pv-top-card-profile-picture__image')?.src;
                    
                    return {
                        name, headline, location, about,
                        experience: expItems.length > 0 ? expItems : null,
                        education: eduItems.length > 0 ? eduItems : null,
                        skills: skills.length > 0 ? skills : null,
                        connections,
                        profileImg
                    };
                }''')
                print(f"[+] Extracted DOM data")
            except Exception as e:
                print(f"[!] DOM extraction error: {e}")
            
            # ============ BUILD DOSSIER ============
            
            # Parse LD+JSON Person data
            person = ld_json_data if ld_json_data.get("@type") == "Person" else {}
            if ld_json_data.get("@type") == "ProfilePage":
                person = ld_json_data.get("mainEntity", {})
            
            # Experience from LD+JSON
            experience = []
            works_for = person.get("worksFor", [])
            if isinstance(works_for, list):
                for job in works_for:
                    experience.append({
                        "title": job.get("name", job.get("jobTitle", "N/A")),
                        "company": job.get("memberOf", {}).get("name") if isinstance(job.get("memberOf"), dict) else job.get("name", ""),
                        "location": job.get("location", "N/A") if isinstance(job.get("location"), str) else (job.get("location", {}).get("name", "N/A") if isinstance(job.get("location"), dict) else "N/A")
                    })
            elif isinstance(works_for, dict):
                experience.append({
                    "title": works_for.get("jobTitle", "N/A"),
                    "company": works_for.get("name", "N/A")
                })
            
            # Education from LD+JSON
            education = []
            alumni_of = person.get("alumniOf", [])
            if isinstance(alumni_of, list):
                for school in alumni_of:
                    education.append({
                        "school": school.get("name", "N/A"),
                        "type": school.get("@type", "N/A")
                    })
            elif isinstance(alumni_of, dict):
                education.append({
                    "school": alumni_of.get("name", "N/A"),
                    "type": alumni_of.get("@type", "N/A")
                })
            
            # Merge DOM experience/education if LD+JSON didn't have them
            if not experience and dom_data.get("experience"):
                experience = dom_data["experience"]
            if not education and dom_data.get("education"):
                education = dom_data["education"]
            
            # Parse connections from meta/description
            connections = dom_data.get("connections", "N/A")
            desc = meta_data.get("og_description", meta_data.get("description", ""))
            if connections == "N/A" or not connections:
                conn_match = re.search(r'([\d,]+)\s*(?:connections|followers)', desc or "", re.IGNORECASE)
                if conn_match:
                    connections = conn_match.group(1)
            
            # Build the dossier
            dossier = {
                "dossier_meta": {
                    "target": f"linkedin.com/in/{username}",
                    "collection_time_utc": datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
                    "clearance_level": "TOP SECRET // LinkedIn Reconnaissance",
                    "voyager_packets_intercepted": len(intercepted_data["voyager"])
                },
                "account_archeology": {
                    "Full_Name": person.get("name", dom_data.get("name", meta_data.get("og_title", "N/A"))),
                    "Headline": dom_data.get("headline", "N/A"),
                    "Location": person.get("address", {}).get("addressLocality", dom_data.get("location", "N/A")) if isinstance(person.get("address"), dict) else dom_data.get("location", "N/A"),
                    "About": dom_data.get("about", person.get("description", "N/A")),
                    "Profile_URL": meta_data.get("og_url", url),
                    "Profile_Image": person.get("image", {}).get("contentUrl", dom_data.get("profileImg", meta_data.get("og_image", "N/A"))) if isinstance(person.get("image"), dict) else dom_data.get("profileImg", meta_data.get("og_image", "N/A")),
                    "Connections": connections
                },
                "professional_intelligence": {
                    "Experience": experience if experience else "N/A",
                    "Education": education if education else "N/A",
                    "Skills": dom_data.get("skills", "N/A"),
                    "Interaction_Type": person.get("interactionStatistic", [{}])[0].get("name", "N/A") if person.get("interactionStatistic") else "N/A"
                },
                "meta_description_raw": desc[:300] if desc else "N/A"
            }
            
            await browser.close()
            return dossier

        except Exception as e:
            print(f"[!] Intelligence Failure: {e}")
            await browser.close()
            return None

async def main():
    username = sys.argv[1] if len(sys.argv) > 1 else "billgates"
    print(f"[*] Initializing LinkedIn Dossier Generation for {username}...")
    
    dossier = await get_linkedin_intel(username)
    
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
