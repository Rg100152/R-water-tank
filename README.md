
# 💧 R Water Tank Platform

> **Premium Water Storage Solutions — Flask + SQLite Web App**
> A corporate-style e-commerce platform for buying and selling water storage tanks.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-black?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 🚀 One-Command Setup (Auto-Install & Run)

**No manual `pip install` needed.** Just run **ONE** command based on your OS:

### 🪟 Windows (PowerShell / CMD)

```powershell
python -m pip install --upgrade pip && pip install flask && python app.py
```

🍎 macOS / 🐧 Linux

```bash
python3 -m pip install --upgrade pip && pip3 install flask && python3 app.py
```

✅ That's it! The app will auto-create the database, install Flask, and launch at
👉 http://127.0.0.1:5000

---

⚡ Ultra-Fast One-Liner (Run Directly From GitHub)

Copy-paste this single line — it will:

1. Clone the repo
2. Install dependencies
3. Run the app automatically

```bash
git clone https://github.com/Rg100152/R-water-tank.git && cd R-water-tank && pip install flask && python app.py
```

---

🖱️ Even Easier: Use the Auto-Run Scripts

The repo includes auto-run scripts that do everything for you.

🪟 Windows Users — Double-Click run.bat

```bat
@echo off
echo ============================================
echo   R WATER TANK - AUTO SETUP ^& LAUNCH
echo ============================================
echo.
echo [1/3] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Download from https://python.org
    pause
    exit /b
)

echo [2/3] Installing dependencies (Flask)...
python -m pip install --upgrade pip --quiet
pip install flask --quiet

echo [3/3] Launching R Water Tank Platform...
echo.
echo ============================================
echo   OPEN: http://127.0.0.1:5000
echo ============================================
echo.
python app.py
pause
```

🍎🐧 macOS / Linux Users — Run run.sh

```bash
#!/bin/bash
echo "============================================"
echo "  R WATER TANK - AUTO SETUP & LAUNCH"
echo "============================================"

echo "[1/3] Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Install it first."
    exit 1
fi

echo "[2/3] Installing Flask..."
python3 -m pip install --upgrade pip --quiet
pip3 install flask --quiet

echo "[3/3] Launching..."
echo "👉 Open: http://127.0.0.1:5000"
python3 app.py
```

Then make it executable:

```bash
chmod +x run.sh
./run.sh
```

---

📦 Requirements

The app only needs one dependency:

Package Version Purpose
flask >=3.0.0 Web framework

requirements.txt (auto-installed by scripts):

```txt
Flask>=3.0.0
```

💡 Everything else (sqlite3, os, random, datetime) is built into Python — no extra installs required.

---

✨ Features

Feature Description
🏠 Home Page Animated hero section with product showcase
🛒 Product Shop Browse tanks from multiple verified sellers
🏢 Seller Portal List your own water tanks with image URLs
📋 Booking System One-click enquiry with unique reference ID
💾 SQLite Database Auto-created on first run — zero setup
🎨 Responsive UI Tailwind CSS + AOS animations
🫧 Animated Loader Water-fill tank loading screen
🖼️ Image Fallbacks Broken images auto-replaced with placeholder

---

🗂️ Project Structure

```
R-water-tank/
├── app.py                  # Main Flask application (all-in-one)
├── requirements.txt        # Python dependencies
├── run.bat                 # Windows auto-run script
├── run.sh                  # macOS/Linux auto-run script
├── r_water_tank_final.db   # SQLite DB (auto-generated)
├── README.md               # This file
└── .gitignore              # Ignores DB, venv, etc.
```

---

🌐 Usage

Once the server starts, open your browser:

URL Page
http://127.0.0.1:5000/ 🏠 Home
http://127.0.0.1:5000/shop 🛒 Browse products
http://127.0.0.1:5000/seller 🏢 Add a product listing
http://127.0.0.1:5000/book/<id> 📋 Book a tank

---

🔧 Manual Setup (If You Prefer Control)

```bash
# 1. Clone
git clone https://github.com/Rg100152/R-water-tank.git
cd R-water-tank

# 2. Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

# 3. Install
pip install -r requirements.txt

# 4. Run
python app.py
```

---

⚙️ Configuration

Setting Location Default
Port app.py → app.run(port=...) 5000
Host app.py → app.run(host=...) 0.0.0.0
Database DB_NAME variable r_water_tank_final.db
Debug mode app.run(debug=...) True

⚠️ Note: The database is reset on every restart (DROP TABLE IF EXISTS) — this keeps demo data fresh. To make it persistent, comment out the DROP TABLE line in init_db().

---

🐛 Troubleshooting

Problem Solution
python: command not found Install Python from python.org and check "Add to PATH"
pip: command not found Use python -m pip instead of pip
Port 5000 already in use Change port in app.py → app.run(port=5001)
Images not loading Your network may block Google image URLs — the app auto-falls back to placeholders
ModuleNotFoundError: flask Run pip install flask again

---

🖼️ Preview Screenshots

Add your screenshots here after first run:

· docs/home.png
· docs/shop.png
· docs/seller.png

---

👨‍💻 Author

Raj Gautam
🎓 BCA 5th Semester
🔗 GitHub: @Rg100152

---

📄 License

This project is open-source and available under the MIT License.
Feel free to fork, modify, and learn from it.

---

<div align="center">

💧 Made with Flask, Tailwind & ❤️

⭐ Star this repo if you found it useful!

</div>
```

---

📁 Additional Files You Should Add to the Repo

1. requirements.txt

```txt
Flask>=3.0.0
```

2. .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
venv/
env/
ENV/
.venv/

# Flask / DB
*.db
*.sqlite
instance/
.env

# IDE
.vscode/
.idea/
*.swp
.DS_Store

# OS
Thumbs.db
```

3. run.bat (Windows auto-runner)

```bat
@echo off
title R Water Tank - Auto Launch
color 0B
echo ============================================
echo   R WATER TANK - AUTO SETUP ^& LAUNCH
echo ============================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not installed!
    echo Download: https://python.org/downloads
    pause
    exit /b
)

echo [1/3] Upgrading pip...
python -m pip install --upgrade pip --quiet

echo [2/3] Installing Flask...
pip install flask --quiet

echo [3/3] Starting server...
echo.
echo ============================================
echo   OPEN: http://127.0.0.1:5000
echo   Press CTRL+C to stop
echo ============================================
echo.
python app.py

pause
```

4. run.sh (macOS/Linux auto-runner)

```bash
#!/bin/bash
echo "============================================"
echo "  R WATER TANK - AUTO SETUP & LAUNCH"
echo "============================================"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not installed. Install it first."
    exit 1
fi

echo "[1/3] Upgrading pip..."
python3 -m pip install --upgrade pip --quiet

echo "[2/3] Installing Flask..."
pip3 install flask --quiet

echo "[3/3] Starting server..."
echo ""
echo "👉 Open: http://127.0.0.1:5000"
echo "   Press CTRL+C to stop"
echo ""
python3 app.py
```

Make it executable after commit:

```bash
git update-index --chmod=+x run.sh
```

---

🎯 How It Works — Auto-Run Flow

```
User runs ONE command
        ↓
┌───────────────────────────────────┐
│  pip install flask  (auto)        │
└───────────────────────────────────┘
        ↓
┌───────────────────────────────────┐
│  python app.py                    │
│    ├─ init_db() → creates SQLite  │
│    └─ app.run() → starts server   │
└───────────────────────────────────┘
        ↓
✅ Browser ready at http://127.0.0.1:5000
```

Total time from clone → running app: ~15 seconds ⚡

---

✅ Final Checklist Before Pushing to GitHub

```bash
# In your project folder
touch requirements.txt .gitignore run.sh run.bat
# (paste content into each from above)

chmod +x run.sh

git add .
git commit -m "Add auto-install README, requirements & run scripts"
git push origin main
```

Once pushed, anyone visiting your repo can just:

1. Click "Code → Download ZIP" or git clone
2. Double-click run.bat (Windows) or run ./run.sh (Mac/Linux)
3. App auto-installs + runs 🚀

---

💡 Bonus: Add a "Run on Replit" Button (optional)

Add this to the top of your README for instant cloud demo:

```markdown
[![Run on Replit](https://replit.com/badge/github/Rg100152/R-water-tank)](https://replit.com/new/github/Rg100152/R-water-tank)
```

This lets anyone test your app online in 10 seconds without installing anything locally — perfect for showcasing to teachers or recruiters! 🎓✨
