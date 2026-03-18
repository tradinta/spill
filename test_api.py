"""Quick test to hit the Flask API and print the raw response."""
import urllib.request
import json
import time

url = "http://localhost:3000/api/extract"
payload = json.dumps({"engine": "tiktok", "target": "tonsic"}).encode("utf-8")
req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})

print(f"[*] Sending POST to {url}...")
start = time.time()
try:
    resp = urllib.request.urlopen(req, timeout=120)
    body = resp.read().decode("utf-8")
    elapsed = time.time() - start
    print(f"[+] Status: {resp.status}  |  Elapsed: {elapsed:.1f}s  |  Body length: {len(body)} chars")
    print(f"[+] First 800 chars of response:\n{body[:800]}")
except Exception as e:
    elapsed = time.time() - start
    print(f"[!] Error after {elapsed:.1f}s: {e}")
