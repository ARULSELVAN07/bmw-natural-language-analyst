from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from bmw_analyst.agent.agent import BMWAnalystAgent
from bmw_analyst.security.logging_config import logger


app = FastAPI(
    title="BMW Natural Language Data Analyst",
    version="1.0.0",
    description="Natural language analytics using MCP and Snowflake.",
)


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Natural language BMW analytics question",
    )


class QuestionResponse(BaseModel):
    question: str
    intent: str
    sql: str
    data: list[dict]
    answer: str


agent = BMWAnalystAgent()


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "bmw-natural-language-analyst",
    }


@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    question = request.question.strip()

    logger.info(
        "API /ask request received length=%s",
        len(question),
    )

    if not question:
        logger.warning("API /ask rejected empty question")
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:
        result = agent.ask(question)

        logger.info(
            "API /ask request completed successfully intent=%s rows=%s",
            result["intent"],
            len(result["data"]),
        )

        return QuestionResponse(
            question=result["question"],
            intent=result["intent"],
            sql=result["sql"],
            data=result["data"],
            answer=result["answer"],
        )

    except ValueError as exc:
        logger.warning(
            "API /ask request rejected error=%s",
            str(exc),
        )

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception:
        logger.exception(
            "API /ask request failed unexpectedly"
        )

        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing the question.",
        )
