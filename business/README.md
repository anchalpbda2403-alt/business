# 🌾 GramBiz AI - AI-Driven Hyperlocal Business Advisory & Financial Structuring Assistant

**GramBiz AI** is a complete, modern, responsive web application designed for rural micro-entrepreneurs in India. It empowers local entrepreneurs to make better business and financial decisions using AI, hyperlocal insights, simple financial structuring tools, automated business plan generation, and expense & revenue management.

---

## 🚀 Key Features

1. **Dashboard & KPIs**: Real-time summary of Monthly Revenue, Monthly Expenses, Estimated Profit, Available Cash, and Funding Need with interactive Chart.js visualizations.
2. **AI Business Health Score**: 0–100 score evaluating Profitability, Expense Control, Cash Reserve, Debt Burden, and Business Stability with strengths, areas for improvement, and next steps.
3. **AI Business Advisor**: Conversational chatbot interface with prompt pills (Business Idea, Increase Sales, Reduce Costs, Funding, Financial Advice) tailored to the entrepreneur's location, budget, and business profile.
4. **Hyperlocal Business Insights**: Local business opportunity evaluation for Indian villages & blocks (Dairy, Food processing, Tailoring, Local handicrafts, Ag services, Grocery, Repair) with demand indicators, investment ranges, and an **"Analyze My Area"** feature.
5. **Financial Structuring & EMI Calculator**: Real-time calculation of total monthly expenses, profit margins, break-even revenue, monthly EMI, funding gap, and 12-month projections.
6. **AI Business Plan Generator**: Form wizard that generates a structured 11-section business plan with print and one-click PDF export capability.
7. **Funding & Loan Guidance**: Structure suggestions (Own contribution, External loan, Trade credit) with informational legal disclaimers.
8. **Expense & Revenue Trackers**: Record daily raw material purchases, transport costs, and product sales with category doughnut charts and sales ranking.
9. **Bilingual Support (English | हिन्दी)**: Instant toggle between English and Hindi text translations across key UI elements.
10. **Mobile First Responsive Design**: Desktop sidebar + mobile touch bottom navigation bar.

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3 (Vanilla CSS with custom design system tokens), JavaScript (Modular Vanilla JS), Chart.js, Font Awesome Icons.
- **Backend**: Python Flask REST API.
- **Database**: MySQL (PyMySQL) with automatic **SQLite fallback** for instant zero-config local testing out-of-the-box.
- **Security**: PBKDF2/Scrypt password hashing via Werkzeug, input sanitization, session authentication.

---

## ⚙️ Local Setup & Installation Instructions

### Step 1: Install Dependencies
Ensure Python 3.8+ is installed on your system. Open terminal or PowerShell in the root project directory:

```bash
pip install -r requirements.txt
```

---

### Step 2: Database Setup (MySQL)

#### Option A: Automatic SQLite (Instant Out-of-the-Box)
No database installation or configuration is required! By default, the application runs on SQLite (`database/grambiz.db`), initializing all tables automatically upon server start.

#### Option B: MySQL Server Setup
1. Start your MySQL Server (e.g. XAMPP, WAMP, or standalone MySQL Server).
2. Create the database and import `schema.sql`:

```bash
mysql -u root -p < database/schema.sql
```

3. Update your `.env` file to enable MySQL:

```env
USE_MYSQL=true
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=grambiz_db
```

---

### Step 3: Setting Environment Variables (`.env`)

Verify your `.env` file at the root of the project:

```env
SECRET_KEY=grambiz_super_secret_key_2026_rural_ai
FLASK_ENV=development
PORT=5000
USE_MYSQL=false
```

---

### Step 4: Running the Flask Application

Run the server using Python:

```bash
python run.py
```

Output:
```
=================================================================
 🌾 GramBiz AI - Hyperlocal Rural Business & Financial Assistant
 🚀 Running locally on: http://127.0.0.1:5000
=================================================================
```

---

### Step 5: Opening the Application

Open your browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

### Step 6: Complete End-to-End Demo Workflow

1. **Landing Page**: Click **"Get Started"** or **"Explore Features"**.
2. **Sign Up**: Fill in your full name, mobile number, email, password, village/town, district, state, and business category.
3. **Onboarding**: Fill in the setup wizard (Initial investment, monthly revenue, monthly expenses, savings, existing loan, and business goals).
4. **Dashboard**: View your **Business Health Score** (e.g. 78/100 Good), Revenue vs Expense chart, and dynamic AI recommendations.
5. **Expense Tracker**: Navigate to **Expenses** -> Add a record (e.g., Date: Today, Category: Raw Material, Amount: 3500) -> View instant chart and table update.
6. **Revenue Tracker**: Navigate to **Revenue** -> Record sales (e.g., Product: Spice Pack, Qty: 20, Amount: 4000).
7. **Financial Planner**: Navigate to **Financial Planner** -> Adjust sliders -> View real-time Break-even revenue, Profit margin %, EMI estimate, and 12-month projected growth graph.
8. **AI Business Advisor**: Navigate to **AI Advisor** -> Click a prompt chip like `💡 Business Idea` or type *"I have ₹50,000. What business can I start?"* -> Receive personalized, profile-aware recommendations.
9. **Business Plan Generator**: Navigate to **Business Plan** -> Fill in details -> Click **"Generate Complete Business Plan"** -> Click **"Download / Print"**.
10. **Language Switcher**: Click the **"हिन्दी"** button in the header topbar to view Indian language translations.

---

### 🔌 Step 7: Connecting a Real External AI API Later (OpenAI / Gemini)

The application features a clean, decoupled service architecture in `backend/services/ai_service.py`. To plug in an external LLM API:

1. Add your API key to `.env`:
   ```env
   OPENAI_API_KEY=sk-...
   # or
   GEMINI_API_KEY=AIzaSy...
   ```
2. In `backend/services/ai_service.py`, update `generate_chat_reply()` or `generate_business_plan()` to forward `user_prompt` and `profile_ctx` to `openai.ChatCompletion.create()` or `google.generativeai.GenerativeModel.generate_content()`.

---

## 📁 Project Structure

```
grambiz-ai/
├── frontend/
│   ├── index.html            # Landing page
│   ├── login.html            # Login authentication
│   ├── signup.html           # Signup page
│   ├── onboarding.html       # Setup wizard
│   ├── dashboard.html        # Main dashboard & KPIs
│   ├── advisor.html          # AI Chatbot interface
│   ├── hyperlocal.html       # Hyperlocal market insights
│   ├── finance.html          # Financial planner & calculator
│   ├── expenses.html         # Expense manager
│   ├── revenue.html          # Revenue tracker
│   ├── business-plan.html    # Business plan generator
│   ├── funding.html          # Funding assistant
│   ├── profile.html          # Profile & notifications
│   ├── css/
│   │   ├── style.css         # Global design tokens
│   │   ├── components.css    # Reusable components
│   │   └── dashboard.css     # Layout grid & navigation
│   └── js/
│       ├── app.js            # Core utilities & notifications
│       ├── auth.js           # Auth & onboarding forms
│       ├── charts.js         # Chart.js graphs
│       ├── i18n.js           # Bilingual switcher
│       ├── advisor.js        # Chatbot streaming
│       └── finance.js        # Calculations & Business Plan PDF
├── backend/
│   ├── app.py                # Flask app entry point
│   ├── config.py             # Config handler
│   ├── database.py           # Database connection & SQLite setup
│   ├── routes/               # API route blueprints
│   │   ├── auth_routes.py
│   │   ├── profile_routes.py
│   │   ├── dashboard_routes.py
│   │   ├── finance_routes.py
│   │   ├── advisor_routes.py
│   │   └── notification_routes.py
│   ├── services/             # Core logic services
│   │   ├── ai_service.py
│   │   ├── financial_engine.py
│   │   └── hyperlocal_service.py
│   └── utils/
│       └── helpers.py
├── database/
│   └── schema.sql            # MySQL schema DDL
├── .env                      # Active environment settings
├── .env.example              # Template
├── requirements.txt          # Python dependencies
├── README.md                 # Complete documentation
└── run.py                    # Root execution script
```
