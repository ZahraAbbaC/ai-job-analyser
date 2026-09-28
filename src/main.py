from fastapi import FastAPI
from pydantic import BaseModel, StringConstraints
from typing import Annotated
from src.analyser import analyse_job


NonEmptyString = Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]

class JobDescription(BaseModel):
    description: NonEmptyString


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Job Analyzer App to be!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/analyse-job")
def analyse_job_endpoint(job: JobDescription):
    analysis_result = analyse_job(job.description)
    return analysis_result