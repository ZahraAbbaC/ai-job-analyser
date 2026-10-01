from pydantic import BaseModel, StringConstraints
from typing import Annotated


NonEmptyString = Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]


class JobDescription(BaseModel):
    description: NonEmptyString


class JobAnalysis(BaseModel):
    word_count: int
    mention_of_python: bool
    mention_of_sql: bool
    mention_of_docker: bool
    mention_of_fastapi: bool


class AIJobAnalysis(BaseModel):
    job_title: str | None
    seniority: str | None
    required_skills: list[str]
    optional_skills: list[str]
    responsibilities: list[str]