import asyncio
import json
import sys
import re
import httpx
from datetime import datetime, timezone
from collections import Counter

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

async def get_reddit_intel(username):
    print(f"[*] Reconnaissance started for Reddit Target: u/{username}")
    
    async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True, timeout=30) as client:
        # 1. Fetch Profile (about.json)
        print("[*] Fetching profile data...")
        about_resp = await client.get(f"https://www.reddit.com/user/{username}/about.json")
        if about_resp.status_code != 200:
            print(f"[!] Failed to fetch profile: {about_resp.status_code}")
            return None
        
        about = about_resp.json().get("data", {})
        print(f"[+] Profile acquired: u/{about.get('name', username)}")
        
        # 2. Fetch Post & Comment History (paginate)
        print("[*] Harvesting post/comment history...")
        all_items = []
        after = None
        for page in range(10):  # Up to 10 pages (~250 items)
            params = {"limit": 100, "sort": "new", "raw_json": 1}
            if after:
                params["after"] = after
            
            resp = await client.get(f"https://www.reddit.com/user/{username}.json", params=params)
            if resp.status_code != 200:
                break
            
            data = resp.json().get("data", {})
            children = data.get("children", [])
            if not children:
                break
            
            all_items.extend(children)
            after = data.get("after")
            if not after:
                break
            
            await asyncio.sleep(1.5)  # Rate limit respect
        
        print(f"[+] Harvested {len(all_items)} items from history")
        
        # 3. Fetch Trophies
        print("[*] Fetching trophies...")
        trophies_list = []
        try:
            trophies_resp = await client.get(f"https://www.reddit.com/user/{username}/trophies.json")
            if trophies_resp.status_code == 200:
                trophies_data = trophies_resp.json().get("data", {}).get("trophies", [])
                trophies_list = [t.get("data", {}).get("name", "Unknown") for t in trophies_data]
        except:
            pass
        
        # ============ ANALYSIS ============
        
        # Separate posts and comments
        posts = [i["data"] for i in all_items if i.get("kind") == "t3"]
        comments = [i["data"] for i in all_items if i.get("kind") == "t1"]
        
        # Sleep Cycle Heatmap (24x7)
        heatmap = {d: {h: 0 for h in range(24)} for d in range(7)}
        timestamps = []
        for item in all_items:
            created = item.get("data", {}).get("created_utc")
            if created:
                dt = datetime.fromtimestamp(created, tz=timezone.utc)
                heatmap[dt.weekday()][dt.hour] += 1
                timestamps.append((dt.hour, dt.weekday()))
        
        # Subreddit Affinity
        subreddit_counts = Counter()
        for item in all_items:
            sub = item.get("data", {}).get("subreddit")
            if sub:
                subreddit_counts[sub] += 1
        top_subreddits = dict(subreddit_counts.most_common(15))
        
        # Interaction Network (who they reply to)
        interaction_targets = Counter()
        for c in comments:
            parent_author = c.get("parent_id", "")
            # We can't directly get parent author from the comment data alone
            # But we can track the subreddit + link context
            link_author = c.get("link_author", "")
            if link_author and link_author != username and link_author != "[deleted]":
                interaction_targets[link_author] += 1
        
        top_interactions = dict(interaction_targets.most_common(10))
        
        # Writing Style Analysis
        all_text = []
        word_counts = []
        for c in comments:
            body = c.get("body", "")
            if body and body != "[deleted]" and body != "[removed]":
                all_text.append(body)
                word_counts.append(len(body.split()))
        
        for p in posts:
            selftext = p.get("selftext", "")
            if selftext and selftext != "[deleted]" and selftext != "[removed]":
                all_text.append(selftext)
                word_counts.append(len(selftext.split()))
        
        # Word frequency (exclude common words)
        stop_words = {"the", "a", "an", "is", "it", "to", "of", "and", "in", "that", "i", "you", "for", "on", "with", "this", "was", "are", "be", "have", "at", "or", "but", "not", "they", "from", "my", "if", "so", "just", "about", "what", "do", "can", "would", "like", "its", "has", "been", "how", "me", "no", "more", "all", "by", "your", "we", "will", "up", "out", "as", "he", "she", "them"}
        all_words = []
        for text in all_text:
            words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
            all_words.extend([w for w in words if w not in stop_words])
        
        word_freq = dict(Counter(all_words).most_common(20))
        
        # Sentiment (simple keyword scoring)
        positive_words = {"good", "great", "love", "awesome", "amazing", "best", "happy", "thanks", "thank", "excellent", "beautiful", "wonderful", "nice", "cool", "fantastic", "perfect", "enjoy", "appreciate", "helpful", "interesting"}
        negative_words = {"bad", "hate", "terrible", "worst", "awful", "horrible", "stupid", "ugly", "boring", "annoying", "sucks", "shit", "damn", "fuck", "hell", "disgusting", "pathetic", "trash", "garbage", "useless"}
        
        pos_count = sum(1 for w in all_words if w in positive_words)
        neg_count = sum(1 for w in all_words if w in negative_words)
        total_sentiment = pos_count + neg_count
        
        # Content type breakdown
        post_types = Counter()
        for p in posts:
            if p.get("is_video"):
                post_types["video"] += 1
            elif p.get("is_gallery"):
                post_types["gallery"] += 1
            elif p.get("selftext"):
                post_types["text"] += 1
            elif p.get("url", "").startswith("https://i."):
                post_types["image"] += 1
            else:
                post_types["link"] += 1
        
        # Top Posts by Score
        top_posts = sorted(posts, key=lambda x: x.get("score", 0), reverse=True)[:5]
        top_posts_data = [{
            "title": p.get("title", "")[:80],
            "subreddit": p.get("subreddit"),
            "score": p.get("score", 0),
            "url": f"https://reddit.com{p.get('permalink', '')}"
        } for p in top_posts]
        
        def format_num(val):
            try: return f"{int(val):,}"
            except: return str(val)
        
        def format_ts(ts):
            if not ts: return "N/A"
            return datetime.fromtimestamp(ts, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        
        # Peak activity
        peak_hour = max(set([t[0] for t in timestamps]), key=[t[0] for t in timestamps].count) if timestamps else "N/A"
        
        # Build Dossier
        dossier = {
            "dossier_meta": {
                "target": f"u/{username}",
                "collection_time_utc": datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
                "clearance_level": "TOP SECRET // Reddit Reconnaissance",
                "items_analyzed": len(all_items)
            },
            "account_archeology": {
                "Display_Name": about.get("subreddit", {}).get("title", about.get("name", "N/A")),
                "Account_Created": format_ts(about.get("created_utc")),
                "Account_Age_Days": (datetime.now(timezone.utc) - datetime.fromtimestamp(about.get("created_utc", 0), tz=timezone.utc)).days if about.get("created_utc") else "N/A",
                "Is_Gold": about.get("is_gold", False),
                "Is_Mod": about.get("is_mod", False),
                "Is_Employee": about.get("is_employee", False),
                "Has_Verified_Email": about.get("has_verified_email", False),
                "Avatar_URL": about.get("icon_img", "N/A").split("?")[0],
                "Trophies": trophies_list
            },
            "karma_breakdown": {
                "Total_Karma": format_num(about.get("total_karma", 0)),
                "Link_Karma": format_num(about.get("link_karma", 0)),
                "Comment_Karma": format_num(about.get("comment_karma", 0)),
                "Awarder_Karma": format_num(about.get("awarder_karma", 0)),
                "Awardee_Karma": format_num(about.get("awardee_karma", 0))
            },
            "behavioral_intelligence": {
                "Sleep_Cycle_Heatmap_UTC": heatmap,
                "Peak_Activity_Hour_UTC": peak_hour,
                "Subreddit_Affinity_Top_15": top_subreddits,
                "Post_Type_Breakdown": dict(post_types),
                "Total_Posts_Analyzed": len(posts),
                "Total_Comments_Analyzed": len(comments)
            },
            "interaction_network": {
                "Top_Reply_Targets": top_interactions
            },
            "writing_style_analysis": {
                "Avg_Word_Count": round(sum(word_counts) / len(word_counts), 1) if word_counts else 0,
                "Max_Word_Count": max(word_counts) if word_counts else 0,
                "Vocabulary_Size_Unique_Words": len(set(all_words)),
                "Top_20_Words": word_freq,
                "Sentiment": {
                    "Positive_Signals": pos_count,
                    "Negative_Signals": neg_count,
                    "Ratio": f"{(pos_count / total_sentiment * 100):.1f}% positive" if total_sentiment > 0 else "N/A"
                }
            },
            "top_posts": top_posts_data
        }
        
        return dossier

async def main():
    username = sys.argv[1] if len(sys.argv) > 1 else "spez"
    print(f"[*] Initializing Reddit Dossier Generation for u/{username}...")
    
    dossier = await get_reddit_intel(username)
    
    if dossier:
        print(json.dumps(dossier, indent=2, ensure_ascii=False))
        print("\n[+] Intelligence Dossier successfully compiled.")
    else:
        print("[!] Failed to compile Intelligence Dossier.")

if __name__ == "__main__":
    asyncio.run(main())
