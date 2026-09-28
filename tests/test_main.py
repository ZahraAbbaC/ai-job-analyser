from src.analyser import analyse_job


def test_ai_job_description_analysis():
    job_description = """
    We are looking for a Junior AI Engineer.
    You should have experience with Python, SQL and Docker.
    Knowledge of FastAPI is a plus.
    """
    expected_result = {
        'word_count': 23,
        'mention_of_python': True,
        'mention_of_sql': True,
        'mention_of_docker': True,
        'mention_of_fastapi': True
    }
    assert analyse_job(job_description) == expected_result

def test_java_job_description_analysis():
    job_description = """
    We are looking for a Java developer with Spring Boot experience.
    """
    expected_result = {
        'word_count': 11,
        'mention_of_python': False,
        'mention_of_sql': False,
        'mention_of_docker': False,
        'mention_of_fastapi': False
    }
    assert analyse_job(job_description) == expected_result

def test_postgresql_job_description_analysis():
    job_description = """
    We are looking for a python developer with PostgreSQL experience.
    """
    expected_result = {
        'word_count': 10,
        'mention_of_python': True,
        'mention_of_sql': False,
        'mention_of_docker': False,
        'mention_of_fastapi': False
    }
    assert analyse_job(job_description) == expected_result