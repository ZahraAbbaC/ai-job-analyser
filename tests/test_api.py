from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import patch
from src.models import AIJobAnalysis


client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyse_job_endpoint():
    response = client.post(
        "/analyse-job",
        json={
            "description": "We are looking for a Junior AI Engineer. You should have experience with Python, SQL and Docker. Knowledge of FastAPI is a plus."
            }
          )
    # print(response.status_code)
    # print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        'word_count': 23,
        'mention_of_python': True,
        'mention_of_sql': True,
        'mention_of_docker': True,
        'mention_of_fastapi': True
    }


def test_analyse_job_requires_description():
    response = client.post(
        "/analyse-job",
        json={
            "wrong_field": "This should fail because the field name is incorrect."
        }
    )

    # print("status code:", response.status_code)
    # print("response:", response.json())
    assert response.status_code == 422


def test_analyse_job_rejects_empty_description():
    response = client.post(
        "/analyse-job",
        json={
            "description": ""
        }
    )
    # print("status code:", response.status_code)
    # print("response:", response.json())
    assert response.status_code == 422


def test_analyse_job_rejects_whitespace_only_description():
    response = client.post(
        "/analyse-job",
        json={
            "description": "   "
        }
    )
    # print("status code:", response.status_code)
    # print("response:", response.json())
    assert response.status_code == 422


def test_analyse_job_rejects_non_string_description():
    response = client.post(
        "/analyse-job",
        json={
            "description": 12345
        }
    )
    # print("status code:", response.status_code)
    # print("response:", response.json())
    assert response.status_code == 422


def test_ai_analyse_job_endpoint_with_mock():
    with patch('src.main.analyse_job_with_ai') as mock_analyse:
        mock_analyse.return_value = AIJobAnalysis(
            job_title="Junior AI Engineer",
            seniority="Junior",
            required_skills=["Python", "FastAPI"],
            optional_skills=["Docker"],
            responsibilities=["Build AI applications"],
        )
        response = client.post(
            "/ai/analyse-job",
            json={
                "description": "We are looking for a Junior AI Engineer."
            }
        )
        assert response.status_code == 200
        assert response.json() == mock_analyse.return_value.model_dump()
        mock_analyse.assert_called_once_with("We are looking for a Junior AI Engineer.")


def test_ai_analyse_job_rejects_empty_description():
    with patch('src.main.analyse_job_with_ai') as mock_analyse:
        response = client.post(
            "/ai/analyse-job",
            json={
                "description": "  "
            }
        )
        assert response.status_code == 422
        mock_analyse.assert_not_called()