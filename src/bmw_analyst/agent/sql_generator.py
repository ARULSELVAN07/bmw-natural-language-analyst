import re
import boto3

from config.settings import (
    AWS_REGION,
    BEDROCK_MODEL_ID,
)

from .prompts import SYSTEM_PROMPT


class SQLGenerator:

    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=AWS_REGION,
        )

    def generate(self, question: str) -> str:

        response = self.client.converse(
            modelId=BEDROCK_MODEL_ID,
            system=[
                {
                    "text": SYSTEM_PROMPT
                }
            ],
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "text": question
                        }
                    ],
                }
            ],
            inferenceConfig={
                "temperature": 0,
                "maxTokens": 1000,
            },
        )

        sql = response["output"]["message"]["content"][0]["text"].strip()

        # Remove markdown fences
        sql = re.sub(
            r"^```(?:sql)?\s*",
            "",
            sql,
            flags=re.IGNORECASE,
        )

        sql = re.sub(
            r"\s*```$",
            "",
            sql,
        )

        # Fix missing spaces after SQL keywords
        sql = re.sub(
            r"\bFROM(?=\S)",
            "FROM ",
            sql,
            flags=re.IGNORECASE,
        )

        sql = re.sub(
            r"\bWHERE(?=\S)",
            "WHERE ",
            sql,
            flags=re.IGNORECASE,
        )

        sql = re.sub(
            r"\bGROUP\s+BY(?=\S)",
            "GROUP BY ",
            sql,
            flags=re.IGNORECASE,
        )

        sql = re.sub(
            r"\bORDER\s+BY(?=\S)",
            "ORDER BY ",
            sql,
            flags=re.IGNORECASE,
        )

        return sql.strip()