<div align="center">

# 🏦 Nexus-Fin

### Personal Finance SaaS — AI-Powered Wealth Planning Engine

[![Stack](https://img.shields.io/badge/Stack-HTML%20%2F%20CSS%20%2F%20JS-blue?style=flat)](https://github.com/MAHAYAVANSHI2904/Nexus-Fin)
[![Finance](https://img.shields.io/badge/Domain-Personal%20Finance-green?style=flat)](#)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat)](LICENSE)

**A client-side personal finance dashboard with a 10-year wealth projection engine and AI-powered spend analysis**  
No backend. No signup. Your data stays in your browser.

[Live Demo](#) · [Features](#features) · [How It Works](#how-it-works)

</div>

---

## Overview

Nexus-Fin is a personal finance SaaS prototype built to solve a specific problem: most budgeting apps show you *where your money went* but not *where it will be* in 5 or 10 years.

Nexus-Fin combines a relational data model (income, expenses, investments, goals) with a compound-growth projection engine that maps your current financial behavior to a long-term wealth curve.

---

## Features

### Wealth Projection Engine
- 10-year net worth projection using compound growth modeling
- Accounts for income growth rate, expense inflation, and investment return assumptions
- Goal-tracking: maps progress to specific financial milestones (emergency fund, home down payment, retirement corpus)
- Monte Carlo-style sensitivity analysis: see best/worst/base case curves

### Expense Intelligence
- Category-level spend breakdown (Housing, Food, Transport, Subscriptions, etc.)
- Month-over-month delta tracking
- AI-powered spend anomaly detection — flags categories trending above 3-month average
- Savings rate calculator with benchmark comparison (50/30/20 rule)

### Investment Tracker
- Multi-asset portfolio view: Equity, Debt, Gold, Real Estate, Crypto
- XIRR-based return calculation per asset class
- Asset allocation heatmap vs target allocation
- SIP tracker with maturity projections

### Dashboard
- Single-page app — zero page reloads
- Dark-mode first, responsive layout
- Exportable reports (PDF snapshot)
- Local storage persistence — all data stays in browser

---

## How It Works

```
User Input (Income / Expenses / Investments / Goals)
              │
              ▼
    Relational Data Model
    ┌─────────────────────────────┐
    │  income[]                   │
    │  expenses[] → categories    │
    │  investments[] → asset_type │
    │  goals[] → target_date      │
    └─────────────────────────────┘
              │
              ▼
    Projection Engine
    - Monthly surplus = income - expenses
    - Invested surplus compounds at user-defined rate
    - Goal gap = target_corpus - projected_value_at_date
              │
              ▼
    Visualization Layer
    - Net worth curve (Chart.js)
    - Category waterfall
    - Goal progress rings
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Vanilla HTML5 + CSS3 (CSS Grid, Custom Properties) |
| Logic | Vanilla JavaScript (ES6+, no framework) |
| Charts | Chart.js |
| Persistence | LocalStorage (relational schema via JSON) |
| AI Analysis | Anthropic Claude API (spend anomaly + advice) |
| Export | html2canvas + jsPDF |

**Why no framework?** Nexus-Fin is intentionally dependency-light. The entire app ships as a single `index.html` — no build step, no `node_modules`, no deploy pipeline. Works offline.

---

## Data Model

```javascript
// Core schema (stored in localStorage as JSON)
{
  income: [
    { id, source, amount, frequency, start_date, growth_rate }
  ],
  expenses: [
    { id, category, description, amount, frequency, is_essential }
  ],
  investments: [
    { id, name, asset_type, current_value, monthly_sip, expected_return, start_date }
  ],
  goals: [
    { id, name, target_amount, target_date, linked_investment_ids[], priority }
  ],
  settings: {
    inflation_rate, risk_profile, currency, salary_growth_rate
  }
}
```

---

## Setup

No installation required. Open `index.html` in any modern browser.

```bash
git clone https://github.com/MAHAYAVANSHI2904/Nexus-Fin.git
cd Nexus-Fin
open index.html   # macOS
# or just drag index.html into Chrome/Firefox
```

For AI-powered spend analysis (optional):
- Get a free API key from [console.anthropic.com](https://console.anthropic.com)
- Enter it in the Settings panel inside the app
- Key is stored only in your browser's localStorage

---

## Roadmap

- [ ] CSV import (bank statements)
- [ ] Indian mutual fund NAV integration (AMFI API)
- [ ] Tax projection module (Old vs New regime comparison)
- [ ] PWA support (offline + installable)
- [ ] Multi-currency support

---

## Security & Privacy

- **No server. No database. No account.** All data lives in your browser.
- AI analysis (if enabled) sends only anonymized spend categories to Claude API — never raw transactions
- Clear data anytime via Settings → Reset

---

## Author

**Chirag Mahayavanshi**  
Senior Finance Executive · ACCA Finalist · Finance + AI Builder  
Mumbai, India

[LinkedIn](https://linkedin.com/in/chiragmahayavanshi) · [GitHub](https://github.com/MAHAYAVANSHI2904) · [Instagram @AiAndAssets](https://instagram.com/aiassets)
