import sys
import json
import subprocess
from datetime import datetime, timezone
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SCRIPT_MAP = {
    'x': 'x_intel.py',
    'reddit': 'reddit_intel.py',
    'tiktok': 'tiktok_intel.py',
    'instagram': 'instagram_intel.py',
    'linkedin': 'linkedin_intel.py',
    'facebook': 'facebook_intel.py'
}

@app.route('/api/extract', methods=['POST'])
def extract_data():
    data = request.json
    engine = data.get('engine')
    target = data.get('target')

    if not engine or not target:
        return jsonify({"error": "Missing engine or target"}), 400

    script_name = SCRIPT_MAP.get(engine)
    if not script_name:
        return jsonify({"error": "Invalid engine"}), 400

    # Clean target for CLI execution safely
    clean_target = target.strip()
    if clean_target.startswith('@'):
        clean_target = clean_target[1:]
    if engine == 'reddit' and clean_target.startswith('u/'):
        clean_target = clean_target[2:]
    if engine == 'facebook' and clean_target.startswith('profile.php?id='):
        clean_target = clean_target.replace('profile.php?id=', '')

    print(f"[*] Starting extraction: {script_name} on {clean_target}")

    try:
        # Run the python script and capture ONLY standard output.
        result = subprocess.run(
            [sys.executable, script_name, clean_target],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=90  # Allow up to 90 seconds for deep scraping
        )
        
        # The python scripts print logs with [*] or [+] prefixes and dump the JSON at the end.
        # We need to extract the JSON payload from the stdout.
        full_output = result.stdout
        
        # Look for the last opening brace { which should be the start of our JSON root object
        try:
            # We attempt a regex or simple split to find the JSON block.
            # Usually the scripts dump cleanly at the very end.
            start_idx = full_output.find('{')
            if start_idx == -1:
                raise ValueError("No JSON payload detected in script output.")
                
            # Parse it recursively or from the first '{' 
            # (Assuming the JSON payload is the main final object printed)
            json_str = full_output[start_idx:]
            
            # Since some scripts might print extra logs, let's reverse search the last closing bracket '}'
            end_idx = json_str.rfind('}')
            if end_idx != -1:
                json_str = json_str[:end_idx+1]
                
            parsed_data = json.loads(json_str)
            
            # Inject target and timestamp so the React frontend header always works
            parsed_data['target'] = target
            parsed_data['timestamp'] = datetime.now(timezone.utc).isoformat()
            
            return jsonify(parsed_data)
            
        except json.JSONDecodeError as decode_err:
            print(f"[!] JSON Decode Target: {repr(full_output)}")
            print(f"[!] Stderr: {result.stderr}")
            return jsonify({
                "error": "Failed to parse JSON from script output",
                "details": str(decode_err),
                "raw_stdout": full_output
            }), 500

    except subprocess.TimeoutExpired:
        return jsonify({"error": "Scraping timed out (90s limit reached). Target may be heavily rate limited."}), 504
    except Exception as e:
        return jsonify({"error": "Internal server execution exception", "details": str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 3000))
    print(f"[*] Starting OSINT Python Microservice on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
