"""
QR Shield — Backend Server
Keeps the Gemini API key hidden on the server.
College students just use the website — no API key needed.

Usage:
  1. pip install flask flask-cors requests
  2. Set your key: set GEMINI_API_KEY=AIza...   (Windows)
                   export GEMINI_API_KEY=AIza... (Linux/Mac)
  3. python server.py
  4. Open http://localhost:5000
"""

import os
import json
import logging
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# ── Config ────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL   = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_URL     = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
PORT           = int(os.environ.get("PORT", 5000))
HOST           = os.environ.get("HOST", "0.0.0.0")   # 0.0.0.0 = accessible on LAN

# Rate limiting (simple in-memory, per IP)
RATE_LIMIT_PER_MINUTE = int(os.environ.get("RATE_LIMIT", 10))

# ── App ───────────────────────────────────────────
app = Flask(__name__, static_folder=".")
CORS(app)  # Allow all origins (college network)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("qrshield")

# ── Simple in-memory rate limiter ─────────────────
import time
from collections import defaultdict

_rate_store = defaultdict(list)

def is_rate_limited(ip: str) -> bool:
    now = time.time()
    window = 60  # 1 minute window
    calls = _rate_store[ip]
    # Remove old calls outside the window
    _rate_store[ip] = [t for t in calls if now - t < window]
    if len(_rate_store[ip]) >= RATE_LIMIT_PER_MINUTE:
        return True
    _rate_store[ip].append(now)
    return False

# ── Routes ────────────────────────────────────────

@app.route("/")
def index():
    """Serve the main HTML page."""
    return send_from_directory(".", "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    """Serve any static asset."""
    return send_from_directory(".", filename)

@app.route("/api/analyze", methods=["POST"])
def analyze():
    """
    Proxy endpoint for Gemini AI analysis.
    Receives: { "url": "...", "staticIssues": [...] }
    Returns:  Gemini analysis JSON
    """
    # Check API key configured
    if not GEMINI_API_KEY:
        return jsonify({
            "error": "API key not configured on server. Contact your administrator.",
            "fallback": True
        }), 503

    # Rate limit check
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if is_rate_limited(client_ip):
        return jsonify({
            "error": f"Too many requests. Please wait a minute. (Limit: {RATE_LIMIT_PER_MINUTE}/min)",
            "rateLimited": True
        }), 429

    # Parse body
    try:
        body = request.get_json(force=True)
        url    = str(body.get("url", "")).strip()[:2000]
        issues = body.get("staticIssues", [])
    except Exception:
        return jsonify({"error": "Invalid request body"}), 400

    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Build prompt
    issues_text = "\n".join(
        f"- [{i.get('severity','?').upper()}] {i.get('title','')}: {i.get('desc','')}"
        for i in issues
    ) or "- No static issues found"

    prompt = f"""You are a world-class cybersecurity expert specializing in phishing detection and QR code security.

Analyze this URL for phishing and security risks:
URL: {url}

Static analysis already identified:
{issues_text}

Respond with ONLY valid JSON (no markdown, no code fences), exactly matching this schema:
{{
  "riskScore": <integer 0-100, 0=completely safe, 100=confirmed critical phishing>,
  "verdict": "<safe|low|medium|high|critical>",
  "verdictLabel": "<Safe|Low Risk|Suspicious|High Risk|Critical Phishing>",
  "summary": "<2-3 clear sentences explaining the risk level and why in plain English>",
  "additionalIssues": [
    {{"title": "...", "desc": "...", "severity": "low|medium|high|critical", "icon": "<emoji>"}}
  ],
  "recommendations": [
    "First clear recommendation",
    "Second clear recommendation",
    "Third clear recommendation"
  ]
}}

Be precise and evidence-based. Consider: social engineering tactics, brand spoofing, phishing URL patterns, credential harvesting, redirect chains, malware delivery indicators."""

    # Call Gemini
    try:
        resp = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.05, "maxOutputTokens": 1200}
            },
            timeout=20
        )
        resp.raise_for_status()
        data = resp.json()
        raw_text = data["candidates"][0]["content"]["parts"][0]["text"]

        # Extract JSON from response
        import re
        match = re.search(r'\{[\s\S]*\}', raw_text)
        if not match:
            raise ValueError("No JSON found in Gemini response")

        result = json.loads(match.group())
        log.info(f"Analyzed URL: {url[:80]} → score={result.get('riskScore','?')} verdict={result.get('verdict','?')}")
        return jsonify(result)

    except requests.exceptions.Timeout:
        return jsonify({"error": "Gemini API timed out. Using static analysis only."}), 504
    except requests.exceptions.HTTPError as e:
        log.error(f"Gemini HTTP error: {e}")
        return jsonify({"error": "Gemini API error. Using static analysis only."}), 502
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        log.error(f"Parse error: {e}")
        return jsonify({"error": "Could not parse AI response. Using static analysis only."}), 500
    except Exception as e:
        log.error(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error."}), 500


@app.route("/api/health")
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "aiEnabled": bool(GEMINI_API_KEY),
        "rateLimit": RATE_LIMIT_PER_MINUTE,
        "model": GEMINI_MODEL
    })


# ── Startup ───────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "="*55)
    print("  🛡️  QR Shield Server")
    print("="*55)
    if GEMINI_API_KEY:
        print(f"  ✅ Gemini AI:  ENABLED ({GEMINI_MODEL})")
    else:
        print("  ⚠️  Gemini AI:  DISABLED (set GEMINI_API_KEY env var)")
    print(f"  🌐 Listening:  http://{HOST}:{PORT}")
    print(f"  📊 Rate limit: {RATE_LIMIT_PER_MINUTE} requests/min per IP")
    print("="*55 + "\n")
    app.run(host=HOST, port=PORT, debug=False)

