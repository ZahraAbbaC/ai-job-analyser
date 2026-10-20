from src.tools import calculate_skill_match


def test_calculate_skill_match_partial_match():
    result = calculate_skill_match(
        required_skills=["Python", "Spark", "Airflow", "AWS", "Kubernetes"],
        candidate_skills=["Python", "SQL", "PostgreSQL", "FastAPI", "Docker"]
    )

    assert result["match_percentage"] == 20.0
    assert set(result["matched_skills"]) == {"python"}
    assert set(result["missing_skills"]) == {
        "spark", "airflow", "aws", "kubernetes"
    }


def test_calculate_skill_match_empty_required_skills():
    result = calculate_skill_match(
        required_skills=[],
        candidate_skills=["python", "SQL"]
    )

    assert result["match_percentage"] == 100
    assert result["matched_skills"] == []
    assert set(result["missing_skills"]) == set()


def test_calculate_skill_match_empty_candidate_skills():
    result = calculate_skill_match(
        required_skills=["python", "aws", "SQL"],
        candidate_skills=[]
    )

    assert result["match_percentage"] == 0
    assert result["matched_skills"] == []
    assert set(result["missing_skills"]) == {"aws", "python", "sql"}


def test_calculate_skill_match_case_differences():
    result = calculate_skill_match(
        required_skills=["Python", "SQL", "AWS", "PostgreSQL"],
        candidate_skills=["Python", "sql", "aws", "Postgresql"]
    )

    assert result["match_percentage"] == 100
    assert set(result["matched_skills"]) == {"python", "sql", "aws", "postgresql"}
    assert set(result["missing_skills"]) == set()


def test_calculate_skill_match_duplicate_skills():
    result = calculate_skill_match(
        required_skills=["Python", "SQL", "AWS", "PostgreSQL"],
        candidate_skills=["Python", "sql", "aws", "aws"]
    )

    assert result["match_percentage"] == 75
    assert set(result["matched_skills"]) == {"python", "sql", "aws"}
    assert set(result["missing_skills"]) == {"postgresql"}
    
