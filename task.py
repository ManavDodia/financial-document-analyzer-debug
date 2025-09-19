## Importing libraries and files
from crewai import Task
from agents import financial_analyst, verifier, risk_assessor
from tools import (
    search_tool,
    read_financial_pdf_tool,
    analyze_investment_data_tool,
    create_risk_assessment_tool
)

# === Task: Analyze Financial Document ===
analyze_financial_document = Task(
    description=(
        "Analyze the provided financial document(s) and the user query: {query}.\n"
        "Scope:\n"
        "1) Identify the document type (e.g., Income Statement, Balance Sheet, Cash Flow, MD&A, 10-K/AR).\n"
        "2) Extract key metrics (revenue, gross margin, operating margin, net income, EPS, FCF, debt, cash, current ratio).\n"
        "3) Compute trends (YoY/ QoQ where possible) and important ratios (profitability, liquidity, leverage, efficiency).\n"
        "4) Summarize drivers, risks, and uncertainties strictly supported by the document.\n"
        "5) If information is missing/ambiguous, explicitly state uncertainties and request needed data.\n"
        "Rules:\n"
        "- Use only available documents/tools. Do not fabricate values or URLs.\n"
        "- If using web search, cite reputable sources and include precise dates.\n"
        "- No personalized investment advice; present findings as informational analysis."
    ),
    expected_output=(
        """{
  "document_type": "<type>",
  "time_coverage": {"start": "<YYYY-MM-DD or FY/Q>", "end": "<YYYY-MM-DD or FY/Q>"},
  "company": "<name if known>",
  "key_metrics": {
    "revenue": {"value": <number>, "unit": "<USD millions>", "period": "<FY/Q>"},
    "gross_margin_pct": <number|null>,
    "operating_margin_pct": <number|null>,
    "net_income": {"value": <number|null>, "unit": "<USD millions>", "period": "<FY/Q>"},
    "free_cash_flow": {"value": <number|null>, "unit": "<USD millions>", "period": "<FY/Q>"},
    "cash": <number|null>, "debt": <number|null>, "current_ratio": <number|null>
  },
  "trends": [{"metric": "<name>", "direction": "up|down|flat", "evidence": "<page/section reference>"}],
  "analysis": [{"topic": "<profitability/liquidity/leverage/efficiency>", "insight": "<concise, evidence-backed>"}],
  "risks_and_uncertainties": [{"risk": "<name>", "evidence": "<doc reference>"}],
  "limitations": ["<explicit unknowns or missing data>"],
  "citations": [{"source": "<doc section or URL>", "accessed": "<YYYY-MM-DD>"}],
  "disclaimer": "This is informational analysis, not investment advice."
}"""
    ),
    agent=financial_analyst,
    async_execution=False,
)

# === Task: Investment Analysis (Informational, not advice) ===
investment_analysis = Task(
    description=(
        "Translate the analysis into scenario-based, informational investment implications for {query}.\n"
        "Scope:\n"
        "1) Summarize valuation context (if inputs available): e.g., P/E, EV/EBITDA, P/S vs peer/5y range.\n"
        "2) Provide neutral scenarios (bull/base/bear) with key drivers and evidence from documents.\n"
        "3) Outline potential catalysts, risks, and checkpoints to monitor (dates, metrics, covenants).\n"
        "4) Clearly separate facts (from docs) from assumptions (label as assumptions).\n"
        "Rules:\n"
        "- No recommendations to buy/sell/hold or product pushing.\n"
        "- No guarantees; no fabricated research; cite any external data.\n"
        "- If peer/market data unavailable, say so and proceed with document-only view."
    ),
    expected_output=(
        """{
  "valuation_snapshot": {
    "pe": {"value": <number|null>, "note": "<if unavailable, say why>"},
    "ev_ebitda": {"value": <number|null>},
    "ps": {"value": <number|null>},
    "peer_context": "<brief or null>"
  },
  "scenarios": [
    {"name": "Bull", "assumptions": ["<list>"], "evidence": ["<doc refs>"], "watch_items": ["<metrics/dates>"]},
    {"name": "Base", "assumptions": ["<list>"], "evidence": ["<doc refs>"], "watch_items": ["<metrics/dates>"]},
    {"name": "Bear", "assumptions": ["<list>"], "evidence": ["<doc refs>"], "watch_items": ["<metrics/dates>"]}
  ],
  "catalysts": ["<events, filings, product launches, macro prints>"],
  "key_risks": ["<from documents or disclosed risk factors>"],
  "monitoring_checklist": ["<KPI1>", "<KPI2>", "<debt covenant>", "<filing date>"],
  "citations": [{"source": "<doc section or URL>", "accessed": "<YYYY-MM-DD>"}],
  "disclaimer": "Educational information only; not investment advice."
}"""
    ),
    agent=financial_analyst,
    async_execution=False,
)

# === Task: Risk Assessment ===
risk_assessment = Task(
    description=(
        "Produce a balanced risk assessment grounded in the financial document(s) for {query}.\n"
        "Scope:\n"
        "1) Identify risk categories: market, credit, liquidity, operational, legal/regulatory.\n"
        "2) Map each risk to evidence in the document and potential impact/probability (qualitative).\n"
        "3) Propose reasonable mitigations and early-warning indicators.\n"
        "Rules:\n"
        "- Do not invent risks or institutions. No extreme claims without evidence.\n"
        "- If data is insufficient to rate a risk, mark it as 'insufficient data'.\n"
        "- Keep language precise and non-alarmist."
    ),
    expected_output=(
        """{
  "risk_register": [
    {
      "category": "market|credit|liquidity|operational|legal",
      "name": "<concise>",
      "evidence": "<doc section/page>",
      "likelihood": "low|medium|high|unknown",
      "impact": "low|medium|high|unknown",
      "mitigations": ["<actions>"],
      "early_indicators": ["<metrics/events>"]
    }
  ],
  "overall_view": "<1–3 sentence summary>",
  "limitations": ["<missing disclosures, stale data, etc.>"],
  "citations": [{"source": "<doc section or URL>", "accessed": "<YYYY-MM-DD>"}],
  "disclaimer": "Risk assessment is informational; not investment advice."
}"""
    ),
    agent=risk_assessor,
    async_execution=False,
)

# === Task: Verification (Document Suitability) ===
verification = Task(
    description=(
        "Verify the uploaded file is a financial document suitable for analysis.\n"
        "Checks:\n"
        "1) File type/structure (parseable text/tables), presence of financial sections (IS/BS/CF, notes, MD&A).\n"
        "2) Period coverage and dates; currency and units.\n"
        "3) Internal consistency (subtotals, totals, footnote references).\n"
        "4) Red flags (images-only scans without text, missing periods, mismatched totals).\n"
        "Rules:\n"
        "- Do not assume; confirm with evidence. If uncertain, report exactly what is missing.\n"
        "- No hallucinations. Do not label non-financial files as financial."
    ),
    expected_output=(
        """{
  "is_financial_document": true|false,
  "document_type": "<type or null>",
  "periods_detected": ["<FY2024>", "<Q1-2025>"],
  "currency_units": "<e.g., USD millions or unknown>",
  "structure_ok": true|false,
  "issues": ["<list concrete parsing/consistency issues>"],
  "next_steps": ["<request specific files/pages or clearer scans>"]
}"""
    ),
    agent=verifier,
    async_execution=False
)
