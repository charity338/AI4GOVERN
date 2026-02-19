# AI4Govern – Public Procurement Risk Monitor

**Author:** Murugi  
**Hackathon:** NIRU AI Hackathon  
**License:** Educational / Hackathon Use

---

## Overview
AI4Govern is an AI-driven governance analytics dashboard designed to flag potential financial and governance risks in public sector projects. The MVP uses historical public procurement and contract award data from Kenya to identify high-risk contracts based on contract value and supplier patterns.

---

## Problem Statement
Public sector projects often face issues such as:

- Cost overruns  
- Delays  
- Limited transparency  

Oversight bodies typically rely on manual review and retrospective audits, which delay intervention. AI4Govern provides a **data-driven tool** to flag high-risk projects early.

---

## Objectives
- Analyze historical public contract award data  
- Identify risk signals based on contract value and supplier repetition  
- Classify projects into **High, Medium, Low Risk**  
- Provide a simple, interactive dashboard for decision-making  

---

## Dataset
- **Source:** World Bank Contract Awards – Investment Project Financing data for Kenya  
- **Time Frame:** Fiscal Years 2020 onwards  
- **Records:** Thousands of contracts  
- **Key Fields:** Contract value, supplier, procurement method, sector, award date  

---

## Methodology
1. **Data cleaning & preprocessing**  
2. **Feature engineering**  
   - Contract value percentiles  
   - Repeat supplier flag  
3. **Risk classification (rule-based)**  
   - High Risk → High contract value + unique supplier  
   - Medium Risk → Other combinations  
   - Low Risk → Low contract value + repeat supplier  
4. **Visualization & dashboard** using Streamlit  

---

## Tools & Technologies
- Python  
- Pandas, NumPy  
- Streamlit (dashboard)  
- GitHub (version control)  

---

## How to Run
1. Clone this repository:  
   ```bash
   git clone <your-repo-url>

## Installation & Running the App

1. **Install requirements:**  
# AI4Govern – Public Procurement Risk Monitor

## Installation & Running the App

1. **Install requirements**  
   `pip install -r requirements.txt`

2. **Run Streamlit app**  
   `streamlit run app.py`

3. **Upload your CSV dataset and explore the dashboard**  

> Step 1 → uses your repo with `app.py`, `requirements.txt`, etc.  
> Step 2 → ensures all packages like Streamlit and Pandas are installed.  
> Step 3 → launches the app.  
> Step 4 → the **sample CSV you provide** is what judges will upload to see the dashboard in action.  

**So the judge sees the end product:** interactive metrics, charts, color-coded tables, top 10 high-risk contracts, etc., **without needing to code anything themselves**.

---

## Features

- **Metrics:** Total contracts, high-risk contracts, total exposure  
- **Charts:** Risk distribution, risk by global practice  
- **Top 10 High-Risk Contracts**  
- **Download high-risk contracts**  
- **Color-coded risk table by signing year**  
- **Supplier insights:** repeat vs unique suppliers  

---

## Expected Impact

- Improve visibility into public spending  
- Highlight high-risk contracts for early intervention  
- Support evidence-based governance and oversight decisions  

---

## Author

**Murugi**




