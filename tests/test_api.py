from fastapi.testclient import TestClient
from src.main import app


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