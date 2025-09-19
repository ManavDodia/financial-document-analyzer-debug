import os
import re
from typing import Any, Dict
from dotenv import load_dotenv

load_dotenv()

# optional import for PDF loader
try:
    from langchain_community.document_loaders import PyPDFLoader
except Exception:
    PyPDFLoader = None

# Do not instantiate SerperDevTool at import time (may subclass BaseTool without _run).
# Instead import lazily inside the wrapper.
def _search_wrapper(query: str) -> str:
    try:
        # import inside function so we don't instantiate at module import
        from crewai_tools import SerperDevTool  # type: ignore
        try:
            tool = SerperDevTool()
            # prefer public run() if present, fallback to _run
            if hasattr(tool, "run"):
                return tool.run(query)
            if hasattr(tool, "_run"):
                return tool._run(query)
            return "[search_tool] SerperDevTool has no runnable method"
        except Exception as e:
            return f"[search_tool] Error instantiating SerperDevTool: {e}"
    except Exception:
        return "[search_tool] SerperDevTool not available"

# export search_tool as plain dict so CrewAI Agent accepts it without coercing BaseTool
search_tool: Dict[str, Any] = {
    "name": "search",
    "func": _search_wrapper,
    "description": "Search wrapper using crewai_tools.SerperDevTool if available"
}

def _clean_text(txt: str) -> str:
    txt = re.sub(r"[ \t]+", " ", txt)
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    return txt.strip()

def read_financial_pdf(path: str) -> str:
    """Load and return cleaned text from a financial PDF"""
    if not path or not os.path.exists(path):
        return f"[read_financial_pdf] File not found: {path}"

    if PyPDFLoader is None:
        return "[read_financial_pdf] PyPDFLoader not available. Install langchain-community."

    try:
        loader = PyPDFLoader(path)
        # handle different loader APIs
        if hasattr(loader, "load_and_split"):
            pages = loader.load_and_split()
        elif hasattr(loader, "load"):
            pages = loader.load()
        else:
            return "[read_financial_pdf] Unsupported PyPDFLoader API."

        if not pages:
            return "[read_financial_pdf] No extractable text (possibly image-only scan)."

        text = "\n\n".join(getattr(p, "page_content", str(p)) for p in pages)
        return _clean_text(text)
    except Exception as e:
        return f"[read_financial_pdf] Error reading PDF: {e}"

def analyze_investment_data(data: str) -> str:
    """Process and analyze financial document data (skeleton)"""
    if not data or data.startswith("[read_financial_pdf]"):
        return "[analyze_investment_data] No valid document text to analyze."
    # placeholder - implement analysis logic here
    return "Investment analysis pipeline not yet implemented."

def create_risk_assessment(data: str) -> str:
    """Create structured risk assessment from financial data (skeleton)"""
    if not data or data.startswith("[read_financial_pdf]"):
        return "[create_risk_assessment] No valid document text to analyze."
    # placeholder - implement risk assessment logic here
    return "Risk assessment pipeline not yet implemented."

# Export tools as plain dictionaries (CrewAI accepts dicts or BaseTool instances)
read_financial_pdf_tool: Dict[str, Any] = {
    "name": "read_financial_pdf",
    "func": read_financial_pdf,
    "description": "Load and return cleaned text from a financial PDF"
}

analyze_investment_data_tool: Dict[str, Any] = {
    "name": "analyze_investment_data",
    "func": analyze_investment_data,
    "description": "Process and analyze financial document data"
}

create_risk_assessment_tool: Dict[str, Any] = {
    "name": "create_risk_assessment",
    "func": create_risk_assessment,
    "description": "Create structured risk assessment from financial data"
}
