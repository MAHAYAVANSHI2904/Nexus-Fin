from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import gspread
from datetime import datetime
import os
import requests
from fpdf import FPDF
from fastapi.responses import Response
import json

app = FastAPI()

# --- CONFIG ---
SHEET_URL = os.getenv("SHEET_URL", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# --- GSHEETS SETUP ---
def get_gsheet_connection():
    if not SHEET_URL:
        print("GSheet Connection Error: SHEET_URL not set")
        return None
    try:
        # Check for service account from env or local file
        creds_json = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
        if creds_json:
            creds_dict = json.loads(creds_json)
            gc = gspread.service_account_from_dict(creds_dict)
        else:
            # Fallback to local file for dev
            base_path = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(os.path.dirname(base_path), 'credentials.json')
            gc = gspread.service_account(filename=filename)
            
        sh = gc.open_by_url(SHEET_URL)
        return sh
    except Exception as e:
        print(f"GSheet Connection Error: {e}")
        return None

# --- MODELS ---
class BudgetData(BaseModel):
    name: str
    designation: str
    income: float
    tier: str
    rent: float
    bills: float
    groceries: float
    commute: float
    sip: float
    bank_save: float
    emergency: float
    dining: float
    shopping: float
    subs: float
    ess: float
    save: float
    life: float
    surplus: float

# --- ENDPOINTS ---

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/budget")
def save_budget(data: BudgetData):
    sh = get_gsheet_connection()
    if not sh:
        raise HTTPException(status_code=500, detail="GSheet Connection Failed")
    
    try:
        # Log Login
        try:
            log_ws = sh.worksheet("Login_Logs")
        except:
            log_ws = sh.add_worksheet(title="Login_Logs", rows=1000, cols=2)
            log_ws.append_row(["User", "Timestamp"])
        log_ws.append_row([data.name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

        # Save Budget Data
        try:
            budget_ws = sh.worksheet("Budget_Data")
        except:
            headers = ["Timestamp", "Name", "Designation", "Income", "Tier", "Rent", "Bills", "Groceries", "Commute", "SIP", "Bank_Save", "Emergency", "Dining", "Shopping", "Subs", "Essentials_Total", "Wealth_Total", "Lifestyle_Total", "Surplus"]
            budget_ws = sh.add_worksheet(title="Budget_Data", rows=1000, cols=len(headers))
            budget_ws.append_row(headers)
        
        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data.name, data.designation, data.income, data.tier,
            data.rent, data.bills, data.groceries, data.commute,
            data.sip, data.bank_save, data.emergency,
            data.dining, data.shopping, data.subs,
            data.ess, data.save, data.life, data.surplus
        ]
        budget_ws.append_row(row)
        return {"status": "success", "message": "Data synced to Google Sheet"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze")
def analyze_budget(data: BudgetData):
    if not GROQ_API_KEY:
        raise HTTPException(status_code=400, detail="Groq API Key missing")
    
    prompt = f"""Act as an Elite AI Financial Architect. Analyze this precise financial blueprint:
    [CLIENT BLUEPRINT]
    - Name: {data.name} | Profession: {data.designation}
    - Monthly Income: Rs.{data.income:,} | Location: {data.tier}
    - Liquidity / Surplus: Rs.{data.surplus:,}
    [EXPENDITURE MATRIX]
    - Essentials (Rs.{data.ess:,}): Rent Rs.{data.rent:,}, Bills Rs.{data.bills:,}, Groceries Rs.{data.groceries:,}, Commute Rs.{data.commute:,}
    - Wealth/Savings (Rs.{data.save:,}): SIPs Rs.{data.sip:,}, Bank Rs.{data.bank_save:,}, Emergency Rs.{data.emergency:,}
    - Lifestyle (Rs.{data.life:,}): Dining Rs.{data.dining:,}, Shopping Rs.{data.shopping:,}, Subs Rs.{data.subs:,}
    [YOUR DIRECTIVES]
    Provide a profound, hyper-modern financial masterplan. Use elite terminology. 
    1. Architectural Summary 2. Risk Analysis 3. Expense Optimization 4. Tax Mastery 5. Asset Allocation 6. Portfolio Picks 7. Peer Benchmarking 8. FIRE Engineering 9. 12-Month Power Move.
    Format as Markdown."""

    try:
        resp = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]}
        )
        res_json = resp.json()
        
        if 'choices' in res_json and len(res_json['choices']) > 0:
            advice = res_json['choices'][0]['message']['content']
        else:
            # Fallback if API fails or returns error
            error_msg = res_json.get('error', {}).get('message', 'Unknown Groq API Error')
            print(f"Groq API Error: {error_msg}")
            
            if "API Key" in error_msg or "Invalid API Key" in error_msg:
                advice = f"### System Notice: API Key Required\n\nNexus Core could not authenticate with the AI services. Please verify your Groq API Key in the backend configuration.\n\n**Immediate Algorithmic Suggestions:**\n1. You have a surplus of **Rs.{data.surplus:,}**. Consider allocating 50% of this to aggressive wealth building (SIPs).\n2. Ensure your Emergency Fund covers at least 6 months of your **Rs.{data.ess:,}** essentials cost.\n3. Keep your lifestyle spending strictly under 30% to maximize FIRE potential."
            else:
                advice = f"### AI Analysis (Fallback Mode)\n\nWe encountered an error analyzing your data: {error_msg}\n\n**Immediate Suggestions:**\n1. You have a surplus of **Rs.{data.surplus:,}**. Consider allocating 50% of this to aggressive wealth building (SIPs).\n2. Ensure your Emergency Fund covers at least 6 months of your **Rs.{data.ess:,}** essentials cost.\n3. Keep your lifestyle spending strictly under 30% to maximize FIRE potential."

        return {"advice": advice}
    except Exception as e:
        print(f"Server Error during analysis: {e}")
        advice = f"### System Warning\n\nCould not connect to AI services. However, your data has been successfully processed.\n\n**Quick Tips:**\n- Keep essentials under 50%.\n- Try to invest at least 20% of your income."
        return {"advice": advice}

@app.post("/api/pdf")
def generate_pdf(data: BudgetData, advice: str):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_fill_color(3,3,10)
        pdf.rect(0,0,210,297,'F')
        
        pdf.set_font("Arial",'B',30)
        pdf.set_text_color(0,255,163)
        pdf.cell(0,40,"ELITE BUDGET TRACKER",0,1,'C')
        
        pdf.set_font("Arial",'',14)
        pdf.set_text_color(150,150,150)
        pdf.cell(0,10,f"STRATEGIC FINANCIAL DOSSIER: {data.name.upper()}",0,1,'C')
        pdf.ln(20)
        
        # KPI Table
        pdf.set_fill_color(20,20,40)
        pdf.set_text_color(255,255,255)
        pdf.set_font("Arial",'B',14)
        pdf.cell(100,12,"  FINANCIAL METRIC",1,0,'L',True)
        pdf.cell(90,12,"  VALUATION",1,1,'L',True)
        
        pdf.set_font("Arial",'',12)
        metrics = [
            ("Monthly Income", f"Rs.{data.income:,}"),
            ("Total Essentials", f"Rs.{data.ess:,}"),
            ("Strategic Wealth", f"Rs.{data.save:,}"),
            ("Lifestyle Spend", f"Rs.{data.life:,}"),
            ("Final Net Surplus", f"Rs.{data.surplus:,}")
        ]
        for l,v in metrics:
            pdf.cell(100,12,f"  {l}",1,0)
            pdf.cell(90,12,f"  {v}",1,1)
        
        pdf.ln(15)
        pdf.set_font("Arial",'B',18)
        pdf.set_text_color(0,255,163)
        pdf.cell(0,15,"ELITE AI AUDIT",0,1)
        
        pdf.set_font("Arial",'',10)
        pdf.set_text_color(220,220,220)
        clean_adv = advice.replace("**","").replace("###","").encode('ascii','ignore').decode('ascii')
        pdf.multi_cell(0,8,f"  {clean_adv}")
        
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=EliteReport_{data.name}.pdf"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
