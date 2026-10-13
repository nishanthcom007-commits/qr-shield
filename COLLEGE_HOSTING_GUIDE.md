# 🛡️ QR Shield — Deployment Guide for College / Public Hosting

QR Shield is pre-configured to work in **Public College Mode**:
- **Students & Teachers need NO API keys.**
- They simply open the website on their phone or laptop, scan or upload any QR code, and get immediate danger scores and full breakdown reports.
- If you configure a single `GEMINI_API_KEY` on your hosting server, the server securely proxies and runs Google Gemini AI for all users with built-in per-IP rate limiting.
- If no key is set, QR Shield still runs **16+ instant offline cybersecurity checks** (detecting HTTP vs HTTPS, brand spoofing, lookalike domains, suspicious TLDs, IP hosts, URL shorteners, etc.).

---

## 🚀 Option 1: Host Inside the College Campus (Local Wi-Fi / LAN)
Any PC or lab machine connected to the college network can host this for everyone on the same Wi-Fi.

1. **Get your local IP address:**
   - In PowerShell / CMD, type: `ipconfig`
   - Look for `IPv4 Address`, e.g., `192.168.1.45` or `10.0.0.12`
2. **Start the server:**
   - Double-click [`start_server.bat`](file:///C:/Users/NISHANTH/.gemini/antigravity/scratch/qr-shield/start_server.bat) OR run:
     ```bash
     set GEMINI_API_KEY=your_gemini_api_key   # Optional: for AI analysis
     python server.py
     ```
3. **Share with college students:**
   - Tell students to connect to college Wi-Fi and open:
     `http://<YOUR_IP>:5000` (e.g. `http://192.168.1.45:5000`)
   - You can even print a QR code linking to `http://<YOUR_IP>:5000` and stick it on college notice boards!

---

## 🌐 Option 2: Host 100% Free on Render.com (Public Internet)
Anyone worldwide or across any mobile network can access it at `https://qrshield-college.onrender.com`.

1. Put the files on GitHub (or upload the folder).
2. Go to [Render.com](https://render.com) (free account) -> **New Web Service**.
3. Choose:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python server.py`
4. Under **Environment Variables**, add:
   - `GEMINI_API_KEY` = your free key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - `PORT` = `10000` (Render default)
5. Click **Deploy Web Service** -> Your public HTTPS link is live!

---

## ☁️ Option 3: Host 100% Free on Railway / HuggingFace Spaces
- **Railway:** Connect repository -> Add variable `GEMINI_API_KEY` -> Railway automatically detects `requirements.txt` & runs `python server.py`.
- **HuggingFace Spaces:** Create a Docker or Python Space, upload `server.py`, `index.html`, and `requirements.txt`. Set Repository Secret `GEMINI_API_KEY`.

---

## 🛡️ Built-in Security & Safety Protections
- **Server-Side Key Hiding:** Your Gemini API key never reaches the student's browser.
- **Built-in Rate Limiter:** Limits requests to 10 per minute per IP to avoid spam or abuse.
- **Dual-Mode Engine:** If the Gemini API experiences network lag, QR Shield automatically falls back to instant static heuristic evaluation so users are never blocked.

