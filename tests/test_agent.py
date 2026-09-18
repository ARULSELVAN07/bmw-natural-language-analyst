from bmw_analyst.agent.agent import BMWAnalystAgent


def test_agent(monkeypatch):

    expected_data = [
        {
            "model": "BMW X5",
            "total_warranty_cost": 95000,
        }
    ]

    agent = BMWAnalystAgent()

    monkeypatch.setattr(
        agent.sql_generator,
        "generate",
        lambda question: """
        SELECT
            model,
            SUM(warranty_cost) AS total_warranty_cost
        FROM BMW_WARRANTY
        GROUP BY model
        ORDER BY total_warranty_cost DESC
        """,
    )

    monkeypatch.setattr(
        "bmw_analyst.agent.agent.execute_query",
        lambda sql: expected_data,
    )

    monkeypatch.setattr(
        agent,
        "generate_narrative",
        lambda question, sql, data:
            "BMW X5 has the highest warranty cost.",
    )

    result = agent.ask(
        "Which BMW model had the highest warranty cost?"
    )

    assert result["question"] == (
        "Which BMW model had the highest warranty cost?"
    )

    assert result["sql"] is not None

    assert result["data"] == expected_data

    assert result["answer"] == (
        "BMW X5 has the highest warranty cost."
    )