import json

import boto3

from config.settings import AWS_REGION, BEDROCK_MODEL_ID
from bmw_analyst.security.sql_validator import validate_sql
from bmw_analyst.mcp_server.server import execute_approved_query

from .prompts import NARRATIVE_PROMPT
from .sql_generator import SQLGenerator


class BMWAnalystAgent:

    def __init__(self):
        self.sql_generator = SQLGenerator()

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
                    "content": [
                        {
                            "text": prompt
                        }
                    ],
                }
            ],
            inferenceConfig={
                "temperature": 0.2,
                "maxTokens": 1000,
            },
        )

        answer = response[
            "output"
        ][
            "message"
        ][
            "content"
        ][0]["text"].strip()

        # Fix common UTF-8 mojibake
        try:
            answer = answer.encode("latin1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass

        return answer

    def ask(self, question: str) -> dict:

        if not question or not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        # --------------------------------------------------
        # 1. Generate SQL using Amazon Bedrock
        # --------------------------------------------------

        sql = self.sql_generator.generate(
            question.strip()
        )

        # --------------------------------------------------
        # 2. Validate generated SQL
        # --------------------------------------------------

        if not validate_sql(sql):
            raise ValueError(
                "Generated SQL failed security validation."
            )

        # --------------------------------------------------
        # 3. Execute through MCP approved tool
        # --------------------------------------------------

        tool_response = execute_approved_query(sql)

        if not tool_response.get("success"):
            raise ValueError(
                tool_response.get(
                    "error",
                    "MCP query execution failed.",
                )
            )

        data = tool_response.get(
            "data",
            [],
        )

        # --------------------------------------------------
        # 4. Generate business explanation
        # --------------------------------------------------

        answer = self.generate_narrative(
            question=question,
            sql=sql,
            data=data,
        )

        # --------------------------------------------------
        # 5. Return final response
        # --------------------------------------------------

        return {
            "question": question,
            "sql": sql,
            "data": data,
            "answer": answer,
        }