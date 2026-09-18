from fastapi.testclient import TestClient

from bmw_analyst.api.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy",
        "service": "bmw-natural-language-analyst",
    }


def test_empty_question():
    response = client.post(
        "/ask",
        json={"question": ""},
    )

    assert response.status_code == 422


def test_missing_question():
    response = client.post(
        "/ask",
        json={},
    )

    assert response.status_code == 422


def test_question_too_long():
    response = client.post(
        "/ask",
        json={
            "question": "A" * 1001,
        },
    )

    assert response.status_code == 422


def test_invalid_json():
    response = client.post(
        "/ask",
        content="not-json",
        headers={
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 422


def test_agent_value_error(monkeypatch):
    from bmw_analyst.api import main

    def mock_ask(question):
        raise ValueError("Generated SQL failed security validation.")

    monkeypatch.setattr(
        main.agent,
        "ask",
        mock_ask,
    )

    response = client.post(
        "/ask",
        json={
            "question": "Show warranty cost",
        },
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Generated SQL failed security validation."
    )


def test_agent_internal_error(monkeypatch):
    from bmw_analyst.api import main

    def mock_ask(question):
        raise RuntimeError("Database connection failed")

    monkeypatch.setattr(
        main.agent,
        "ask",
        mock_ask,
    )

    response = client.post(
        "/ask",
        json={
            "question": "Show warranty cost",
        },
    )

    assert response.status_code == 500

    assert response.json()["detail"] == (
        "An internal error occurred while processing the question."
    )


def test_successful_question(monkeypatch):
    from bmw_analyst.api import main

    expected_result = {
        "question": "Which model had the highest warranty cost?",
        "intent": "warranty_cost",
        "sql": (
            "SELECT model, SUM(warranty_cost) "
            "FROM BMW_ANALYTICS.BMW_DATA.BMW_WARRANTY "
            "GROUP BY model"
        ),
        "data": [
            {
                "MODEL": "BMW X5",
                "SUM(WARRANTY_COST)": 95000,
            }
        ],
        "answer": "BMW X5 had the highest warranty cost.",
    }

    def mock_ask(question):
        return expected_result

    monkeypatch.setattr(
        main.agent,
        "ask",
        mock_ask,
    )

    response = client.post(
        "/ask",
        json={
            "question": "Which model had the highest warranty cost?",
        },
    )

    assert response.status_code == 200

    result = response.json()

    assert result["question"] == expected_result["question"]
    assert result["intent"] == expected_result["intent"]
    assert result["sql"] == expected_result["sql"]
    assert result["data"] == expected_result["data"]
    assert result["answer"] == expected_result["answer"]