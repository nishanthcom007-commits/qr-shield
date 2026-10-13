# 🛡️ QR Shield — Anti-Quishing & QRLJacking Defense Engine

> **Live Demo →** [https://YOUR-USERNAME.github.io/qr-shield](https://YOUR-USERNAME.github.io/qr-shield)

A modern, single-page cybersecurity web application built for the **IDT Lab** that detects and neutralizes QR code-based threats — including Quishing attacks, QRLJacking session hijacks, Typo-Squatting domains, and fraudulent UPI payment requests — **before** the device executes the payload.

---

## 🚨 Why QR Codes Are Dangerous

A QR code is a **2D binary matrix** (ISO/IEC 18004) encoding up to 4,296 characters. Unlike hyperlinks rendered as readable text, the embedded payload is **entirely invisible to the human eye** prior to execution. QR Shield intercepts and decodes that payload *before* the device acts on it.

---

## ✨ Features

| Module | Description |
|---|---|
| 🔍 **Pre-Execution Payload Analyzer** | Paste any QR payload for instant 4-layer inspection |
| 🧱 **4-Layer Rule Engine** | Transport · Typo-Squat · QRLJacking · UPI Whitelist |
| 📊 **Threat Gauge** | Weighted risk score 0–100 with verdict banners |
| 🏴 **QRLJacking Sandbox** | Simulated deceptive campus flyer with attack walkthrough |
| 🏗️ **Architecture Summary** | IDT Lab methodology: Input → Processing → Mitigation |

---

## 🔬 4-Layer Inspection Engine

```
Layer 1 — Transport Encryption & Scheme Integrity
  ↳ Validates HTTPS vs insecure HTTP; detects non-standard URI schemes

Layer 2 — Typo-Squatting & Domain Spoofing Detection
  ↳ Levenshtein distance vs trusted domains · Suspicious TLDs · Multi-level subdomain chains

Layer 3 — QRLJacking & Session-Pairing Intercept
  ↳ Detects: pair?token=, auth-token, session/pair, linked-device, oauth-callback

Layer 4 — Campus Merchant Whitelist (UPI VPA Validator)
  ↳ Validates UPI VPAs against registered campus merchant accounts
```

---

## 🧪 Sample Test Vectors

| Vector | Payload | Expected Result |
|---|---|---|
| ✅ Clean | `https://vtu.ac.in/examination-results/` | **SAFE** (Score: 0) |
| ⚠️ Vector A | `http://vtu-resu1ts.ac.in.secure-login.xyz/token=491` | **SUSPICIOUS** |
| 🚨 Vector B | `https://web.whatsapp.com-auth-token.xyz/session/pair?token=8f9a21b` | **CRITICAL** |
| ⚠️ Vector C | `upi://pay?pa=attacker982@paytm&pn=RefundDesk` | **SUSPICIOUS** |
| ✅ Vector D | `upi://pay?pa=campus.canteen@okhdfcbank&pn=CollegeCanteen` | **SAFE** |

---

## 🏗️ Tech Stack

- **HTML5** — Semantic single-page structure
- **Tailwind CSS** (CDN) — Utility-first styling with custom dark theme
- **Vanilla JavaScript** — Zero-dependency analysis engine
- **Font Awesome 6** — Icon badges
- **JetBrains Mono** — Monospace log & code rendering

---

## 🚀 Hosting on GitHub Pages

1. Push this repo to GitHub
2. Go to **Settings → Pages**
3. Set source to **Deploy from branch → `main` → `/ (root)`**
4. Your site will be live at `https://YOUR-USERNAME.github.io/qr-shield`

---

## 📁 Project Structure

```
qr-shield/
├── index.html      ← Complete single-page application
├── .gitignore
└── README.md
```

---

## ⚠️ Disclaimer

This tool is built for **educational and research purposes** as part of the IDT Lab curriculum. The QRLJacking sandbox demonstrates attack vectors in a controlled, ethical environment. Do not use this knowledge for malicious purposes.

---

## 👨‍💻 IDT Lab — Cybersecurity Research

Built with ❤️ for campus security awareness.

