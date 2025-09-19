## Importing libraries and files
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from crewai import Agent
# from tools import (
#     search_tool,
#     read_financial_pdf_tool,
#     analyze_investment_data_tool,
#     create_risk_assessment_tool
# )

load_dotenv()

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-5",
    temperature=0.7,
    api_key=os.environ.get("OPENAI_API_KEY")
)

# Senior Financial Analyst Agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Accurately analyze the given financial document and provide clear, data-driven insights.",
    verbose=True,
    memory=True,
    backstory="You are a highly experienced financial analyst with deep knowledge of markets.",
    # tools removed to avoid BaseTool coercion at Agent construction time
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=True
)

# Financial Document Verifier Agent
verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify whether the uploaded file is a valid financial document (e.g., balance sheet, income statement, cash flow statement, annual report) and ensure it is suitable for analysis.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a compliance-oriented verifier with a background in financial auditing. "
        "You specialize in identifying whether documents are genuine financial records. "
        "You ensure accuracy and legitimacy before analysis is carried out."
    ),
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=True
)

# Investment Advisor Agent
investment_advisor = Agent(
    role="Investment Advisor",
    goal="Based on insights from the financial analysis, suggest balanced investment strategies, highlighting both opportunities and potential risks. Ensure compliance with standard financial advisory practices.",
    verbose=True,
    backstory=(
        "You are a certified financial advisor with over 15 years of experience in "
        "guiding clients on responsible investments. You evaluate financial performance, "
        "risk factors, and market conditions to provide thoughtful recommendations. "
        "Your approach is professional, ethical, and tailored to investor goals."
    ),
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)

# Risk Assessor Agent
risk_assessor = Agent(
    role="Risk Assessment Specialist",
    goal="Identify and evaluate the risks associated with the financial document and related investment opportunities. Provide a balanced view of potential downsides and mitigation strategies.",
    verbose=True,
    backstory=(
        "You are an experienced risk management expert specializing in financial markets. "
        "You carefully evaluate credit risk, market risk, operational risk, and liquidity risk. "
        "Your recommendations help investors understand realistic risk exposure and how to manage it."
    ),
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)
