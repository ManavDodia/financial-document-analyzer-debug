from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid

from crewai import Crew, Process
from agents import financial_analyst
from task import analyze_financial_document  # Make sure this is the only task we're importing

app = FastAPI(title="Financial Document Analyzer")

def run_crew(query: str, file_path: str) -> str:
    """Run the crew with the current query and file path."""
    financial_crew = Crew(
        agents=[financial_analyst],
        tasks=[analyze_financial_document],
        process=Process.sequential,
    )
    result = financial_crew.kickoff({"query": query, "file_path": file_path})
    return str(result)

@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_endpoint(  # renamed to avoid clashing with imported Task
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights"),
):
    """Analyze a financial document and return structured findings."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=415, detail="Only PDF files are supported.")

    file_id = str(uuid.uuid4())
    os.makedirs("data", exist_ok=True)
    file_path = f"data/financial_document_{file_id}.pdf"

    try:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Empty file uploaded.")
        with open(file_path, "wb") as f:
            f.write(content)

        query = (query or "").strip() or "Analyze this financial document for investment insights"
        analysis = run_crew(query=query, file_path=file_path)

        return {
            "status": "success",
            "query": query,
            "analysis": analysis,
            "file_processed": file.filename,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {e}")
    finally:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass
