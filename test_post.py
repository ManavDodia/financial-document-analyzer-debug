import requests
from pathlib import Path

pdf_path = Path(r"C:\Users\manav\Desktop\financial-document-analyzer-debug\data\TSLA-Q2-2025-Update.pdf")
if not pdf_path.exists():
    raise SystemExit(f"PDF not found: {pdf_path}")

with pdf_path.open("rb") as f:
    files = {"file": ("TSLA-Q2-2025-Update.pdf", f, "application/pdf")}
    data = {"query": "Extract key metrics, trends and risks from this Q2 update"}
    try:
        r = requests.post("http://127.0.0.1:8000/analyze", files=files, data=data, timeout=30)
        print(r.status_code)
        print(r.headers.get("content-type"))
        print(r.text[:2000])  # print first 2000 chars
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)