<div align="center">

# 🏦 Nexus-Fin

### Personal Finance SaaS — AI-Powered Wealth Planning Engine

[![Frontend](https://img.shields.io/badge/Frontend-HTML%20%2F%20CSS%20%2F%20JS-blue?style=flat)](https://github.com/MAHAYAVANSHI2904/Nexus-Fin)
[![Backend](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![AI](https://img.shields.io/badge/AI-Groq%20LLaMA%203.3-F55036?style=flat)](https://groq.com)
[![Sheets](https://img.shields.io/badge/Storage-Google%20Sheets-34A853?style=flat&logo=googlesheets&logoColor=white)](https://www.google.com/sheets/about/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat)](LICENSE)

**A personal finance dashboard with AI-powered budget analysis and a downloadable wealth report — built on a lightweight FastAPI backend**

[Features](#features) · [Architecture](#architecture) · [Setup](#setup)

</div>

---

## Overview

Nexus-Fin helps users map their income, expenses, and savings into a clear budget breakdown — then sends that breakdown to an LLM for personalized financial analysis, and exports the whole thing as a styled PDF report.

The frontend is a single-page HTML/CSS/JS app. The backend is a small FastAPI service that handles three jobs: log budget data to Google Sheets, get AI analysis from Groq, and generate a PDF report.

---

## Features

### Budget Input & Breakdown
- Structured input across three categories: Essentials (rent, bills, groceries, commute), Wealth (SIPs, bank savings, emergency fund), Lifestyle (dining, shopping, subscriptions)
- Auto-calculated totals and surplus
- City-tier aware (Tier 1/2/3) for context-appropriate suggestions

### AI Financial Analysis
- Sends the full budget blueprint to Groq's LLaMA 3.3 70B model
- Structured output: Risk Analysis, Expense Optimization, Tax Strategy, Asset Allocation, Portfolio Suggestions, Peer Benchmarking, FIRE Planning, and a 12-month action plan
- Graceful fallback with rule-based suggestions if the AI call fails — the app never breaks

### Google Sheets Logging
- Every submission logs to two sheets: `Login_Logs` (who, when) and `Budget_Data` (full breakdown)
- Sheets auto-created on first run if they don't exist
- Useful for tracking usage and building a dataset over time

### PDF Report Export
- Generates a styled, dark-themed PDF with the full budget table and AI analysis
- One-click download, named after the user

---

## Architecture

```
┌─────────────────┐         ┌──────────────────┐
│  Frontend        │  POST   │  FastAPI Backend  │
│  (index.html)    │ ──────► │  (backend/main.py)│
│  Budget Form     │         │                   │
└─────────────────┘         └─────────┬─────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                   ▼                   ▼
            ┌───────────────┐  ┌───────────────┐  ┌──────────────┐
            │ Google Sheets  │  │  Groq API      │  │  FPDF        │
            │ (data log)     │  │  (AI analysis) │  │ (PDF export) │
            └───────────────┘  └───────────────┘  └──────────────┘
```

### Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/health` | GET | Health check |
| `/api/budget` | POST | Log budget submission to Google Sheets |
| `/api/analyze` | POST | Get AI financial analysis from Groq |
| `/api/pdf` | POST | Generate downloadable PDF report |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Vanilla JS |
| Backend | FastAPI, Pydantic |
| AI | Groq API — `llama-3.3-70b-versatile` |
| Data Logging | Google Sheets via gspread |
| PDF Generation | fpdf2 |
| Server | Uvicorn |

---

## Setup

### Prerequisites
- Python 3.10+
- Groq API key (free tier works): [console.groq.com](https://console.groq.com)
- Google Cloud service account with Sheets API access (optional, for data logging)

### 1. Clone

```bash
git clone https://github.com/MAHAYAVANSHI2904/Nexus-Fin.git
cd Nexus-Fin
```

### 2. Backend setup

```bash
cd backend
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your values:

```bash
cp ../.env.example .env
```

```env
GROQ_API_KEY=gsk_your_key_here
SHEET_URL=https://docs.google.com/spreadsheets/d/your_sheet_id/edit
GOOGLE_SHEETS_CREDENTIALS={"type":"service_account",...}
```

> **Note:** `SHEET_URL` and `GOOGLE_SHEETS_CREDENTIALS` are optional. Without them, budget logging is skipped but AI analysis and PDF export still work.

### 3. Run the backend

```bash
uvicorn main:app --reload --port 8000
```

### 4. Open the frontend

Open `index.html` in your browser. Update the API base URL inside the JS to point to `http://localhost:8000` if running locally.

---

## Security

- No API keys, credentials, or sheet IDs committed to this repo
- All secrets loaded via environment variables — see `.env.example`
- `.gitignore` covers `.env`, `credentials.json`, and `*.pem`
- AI analysis includes a graceful fallback path — app stays functional even if the Groq API key is missing or the call fails

---

## Author

**Chirag Mahayavanshi**  
Senior Finance Executive · ACCA Finalist · Finance + AI Builder  
Mumbai, India

[LinkedIn](https://www.linkedin.com/in/mahayavanshic/) · [GitHub](https://github.com/MAHAYAVANSHI2904)
