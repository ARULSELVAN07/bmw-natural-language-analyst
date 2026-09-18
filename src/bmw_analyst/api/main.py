from fastapi import FastAPI, HTTPException

from bmw_analyst.models.schemas import (
    AnalysisResponse,
    QuestionRequest,
)

from bmw_analyst.agent.agent import BMWAnalystAgent


app = FastAPI(
    title="BMW Natural Language Analyst",
    description=(
        "Natural language BMW analytics "
        "using MCP, Amazon Bedrock and Snowflake."
    ),
    version="1.0.0",
)


agent = BMWAnalystAgent()


@app.get("/")
def root():
    return {
        "application": "BMW Natural Language Analyst",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post(
    "/ask",
    response_model=AnalysisResponse,
)
def ask_question(
    request: QuestionRequest,
):
    try:
        result = agent.ask(request.question)

        return AnalysisResponse(
            **result
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
    