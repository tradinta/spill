"""Test ALL 6 engines and dump their response structure (top-level keys)."""
import urllib.request
import json
import time

url = "http://localhost:3000/api/extract"

tests = [
    {"engine": "tiktok", "target": "tonsic"},
    {"engine": "x", "target": "elonmusk"},
    {"engine": "reddit", "target": "spez"},
    {"engine": "instagram", "target": "zuck"},
    {"engine": "linkedin", "target": "satyanadella"},
    {"engine": "facebook", "target": "zuck"},
]

for t in tests:
    payload = json.dumps(t).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    print(f"\n{'='*60}")
    print(f"[*] Testing: engine={t['engine']}  target={t['target']}")
    start = time.time()
    try:
        resp = urllib.request.urlopen(req, timeout=120)
        body = resp.read().decode("utf-8")
        data = json.loads(body)
        elapsed = time.time() - start
        print(f"[+] Status: {resp.status}  |  Elapsed: {elapsed:.1f}s")
        print(f"[+] Top-level keys: {list(data.keys())}")
        # Check if 'target' and 'timestamp' fields exist
        print(f"    has 'target': {'target' in data}")
        print(f"    has 'timestamp': {'timestamp' in data}")
        print(f"[+] First 300 chars: {body[:300]}")
    except Exception as e:
        elapsed = time.time() - start
        print(f"[!] Error after {elapsed:.1f}s: {e}")
        try:
            err_body = e.read().decode("utf-8") if hasattr(e, 'read') else ''
            print(f"    Response: {err_body[:300]}")
        except:
            pass
