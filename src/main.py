from fastapi import FastAPI
from src.analyser import analyse_job
from src.ai_analyser import analyse_job_with_ai
from src.models import JobDescription, JobAnalysis, AIJobAnalysis


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Job Analyzer App to be!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/analyse-job", response_model=JobAnalysis)
def analyse_job_endpoint(job: JobDescription):
    analysis_result = analyse_job(job.description)
    return analysis_result

@app.post("/ai/analyse-job", response_model=AIJobAnalysis)
def ai_analyse_job_endpoint(job: JobDescription):
    analysis_result = analyse_job_with_ai(job.description)
    return analysis_result