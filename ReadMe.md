# Dennis & Elvie Fish Processing — Management System

## Requirements
- Python 3.12 (exactly – newer versions may not work)
- Visual Studio Code (or any text editor)

---

## Setup Instructions

### Step 1 — Install Python
Download from https://python.org and install (check "Add to PATH").

### Step 2 — Open the project in VS Code
Open the `TinapaWeb` folder in VS Code.

### Step 3 — Open a terminal
In VS Code: `Terminal > New Terminal`

### Step 4 — Create a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate (Windows)
source venv/bin/activate (Mac/Linux)

### Step 5 — Install dependencies
pip install -r requirements.txt


### Step 6 — Run the app
python main.py


### Step 7 — Open in browser
Go to: http://localhost:5000

---

## Login Credentials

| Role  | Email                           | Password |
|-------|---------------------------------|----------|
| Admin | franciscorayver20@gmail.com     | admin123 |

Regular staff accounts can be created by the admin.

---

## Features
- Secure login with Role‑Based Access Control (Admin / Staff)
- Product inventory with daily sheets (Smoked/Dried, units, stock, status badges)
- **Transactions** – create delivery boxes, add products, track total price
- **Personnel management** – add/update/delete staff, change status (Available / On Duty / Unavailable)
- **Transaction History** – archive and restore sheets, export to Excel
- **Admin Panel** – manage user accounts (add/edit/delete, set roles)
- Real‑time updates (polling) – no manual refresh needed
- Fully responsive design (works on mobile)

---

## Project Files
TinapaWeb/
├── main.py ← Entry point
├── requirements.txt ← Dependencies
├── runtime.txt ← Python version lock (3.12)
├── README.md ← This file
├── website/ ← Core application
│ ├── init.py ← App factory, config
│ ├── models.py ← Database schemas
│ ├── auth.py ← Login & RBAC logic
│ ├── views.py ← Main routes
│ ├── templates/ ← HTML pages
│ └── static/ ← CSS, JS (index.js)
├── instance/ ← SQLite database (auto-created)
└── .gitignore ← Excludes venv, .db, .env, etc.

---

## Live Demo (after deployment)
The application will be hosted at: `https://your-app-name.onrender.com` (or your chosen platform).

---

## Contributors
- @franciscorayver20-glitch