from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from uuid import uuid4

from bmw_analyst.agent.agent import BMWAnalystAgent
from bmw_analyst.api.metrics import increment, snapshot
from config.settings import API_KEY
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


@app.middleware("http")
async def request_context(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid4())
    request.state.request_id = request_id
    increment("http_requests_total")

    try:
        response = await call_next(request)
    except Exception:
        increment("http_requests_failed_total")
        raise

    response.headers["X-Request-ID"] = request_id
    logger.info(
        "HTTP request completed request_id=%s method=%s path=%s status=%s",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
    )
    return response


def _require_api_key(path: str, provided_key: str | None) -> None:
    if path in {"/health", "/ready", "/metrics", "/openapi.json", "/docs"}:
        return
    if API_KEY and provided_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "bmw-natural-language-analyst",
    }


@app.get("/ready")
def readiness(x_api_key: str | None = Header(default=None)):
    _require_api_key("/ready", x_api_key)
    from bmw_analyst.snowflake.connection import get_connection

    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        return {"status": "ready", "service": "bmw-natural-language-analyst"}
    except Exception:
        logger.exception("Readiness check failed")
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "service": "bmw-natural-language-analyst"},
        )
    finally:
        if connection is not None:
            connection.close()


@app.get("/metrics")
def metrics():
    return snapshot()


@app.post("/ask", response_model=QuestionResponse)
def ask_question(
    http_request: Request,
    request: QuestionRequest,
    x_api_key: str | None = Header(default=None),
):
    _require_api_key("/ask", x_api_key)
    question = request.question.strip()
    request_id = getattr(http_request.state, "request_id", "unknown")

    logger.info(
        "API /ask request received request_id=%s length=%s",
        request_id,
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
            "API /ask request completed request_id=%s intent=%s rows=%s",
            request_id,
            result["intent"],
            len(result["data"]),
        )
        increment("ask_requests_succeeded_total")

        return QuestionResponse(
            question=result["question"],
            intent=result["intent"],
            sql=result["sql"],
            data=result["data"],
            answer=result["answer"],
        )

    except ValueError as exc:
        increment("ask_requests_rejected_total")
        logger.warning(
            "API /ask request rejected error=%s",
            str(exc),
        )

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception:
        increment("ask_requests_failed_total")
        logger.exception(
            "API /ask request failed unexpectedly"
        )

        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing the question.",
        )
