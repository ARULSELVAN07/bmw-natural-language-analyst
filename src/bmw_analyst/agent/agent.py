import asyncio
import json
import boto3

from config.settings import AWS_REGION, BEDROCK_MODEL_ID
from bmw_analyst.security.sql_validator import validate_sql
from bmw_analyst.security.logging_config import logger
from bmw_analyst.mcp_client.client import MCPClient

from .prompts import NARRATIVE_PROMPT
from .router import IntentRouter
from .sql_generator import SQLGenerator


class BMWAnalystAgent:

    def __init__(self):
        self.sql_generator = SQLGenerator()
        self.mcp_client = MCPClient()
        self.intent_router = IntentRouter()

        self.client = boto3.client(
            "bedrock-runtime",
            region_name=AWS_REGION,
        )

    def generate_narrative(
        self,
        question: str,
        sql: str,
        data: list[dict],
    ) -> str:

        logger.info("Generating narrative response")

        prompt = f"""
User question:
{question}

SQL:
{sql}

Query result:
{json.dumps(data, default=str)}

{NARRATIVE_PROMPT}
"""

        response = self.client.converse(
            modelId=BEDROCK_MODEL_ID,
            messages=[
                {
                    "role": "user",
                    "content": [{"text": prompt}],
                }
            ],
            inferenceConfig={
                "temperature": 0.2,
                "maxTokens": 1000,
            },
        )

        answer = (
            response["output"]["message"]["content"][0]["text"]
            .strip()
        )

        try:
            answer = answer.encode("latin1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass

        logger.info("Narrative response generated successfully")

        return answer

    def ask(self, question: str) -> dict:

        if not question or not question.strip():
            logger.warning("Empty question received")
            raise ValueError("Question cannot be empty.")

        question = question.strip()

        logger.info(
            "Analyst question received length=%s",
            len(question),
        )

        intent = self.intent_router.route(question)

        logger.info(
            "Intent detected intent=%s",
            intent.value,
        )

        sql = self.sql_generator.generate(question)

        logger.info("SQL generated successfully")

        if not validate_sql(sql):
            logger.warning(
                "Generated SQL failed security validation"
            )
            raise ValueError(
                "Generated SQL failed security validation."
            )

        logger.info("Generated SQL passed security validation")

        tool_response = asyncio.run(
            self.mcp_client.execute_approved_query(sql)
        )

        if not tool_response.success:
            logger.error(
                "MCP query execution failed error=%s",
                tool_response.error,
            )

            raise ValueError(
                tool_response.error
                or "MCP query execution failed."
            )

        data = tool_response.data

        logger.info(
            "MCP query completed rows_returned=%s",
            len(data),
        )

        answer = self.generate_narrative(
            question=question,
            sql=sql,
            data=data,
        )

        logger.info("Analyst request completed successfully")

        return {
            "question": question,
            "intent": intent.value,
            "sql": sql,
            "data": data,
            "answer": answer,
        }