import openai
from dotenv import load_dotenv
from openai import OpenAI    
from src.models import AIJobAnalysis
from src.exceptions import AIServiceError


load_dotenv()  # Load environment variables from .env file


client = OpenAI()  # Create an OpenAI client instance



def analyse_job_with_ai(description: str):
    try:
        response = client.responses.parse(
            model = "gpt-4o-mini",
            input = [
                {"role": "system", 
                 "content": """You are a helpful assistant that extracts structured information from job descriptions. 
                    Extract only information supported by the job description.
                    Do not invent requirements that are not stated or reasonably implied."""},
                {"role": "user", 
                 "content": f"""Analyse the following job description:
                    \n{description}"""}
            ],
            text_format = AIJobAnalysis
        )
        return response.output_parsed  # Return the parsed structured data as an AIJobAnalysis instance
    except openai.APIConnectionError as e:
        raise AIServiceError("Could not connect to AI service.") from e
    except openai.RateLimitError as e:
        raise AIServiceError("AI service rate limit exceeded.") from e
    except openai.InternalServerError as e:
        raise AIServiceError("AI service encountered an internal error.") from e
    


if __name__ == "__main__":
    job1 = """
    We are looking for a Junior AI Engineer to join our team.
    The candidate should have experience with Python, FastAPI,
    PostgreSQL and Docker. Experience building LLM applications
    and RAG pipelines is preferred.
    """

    job2 = """
    You will build intelligent internal tools that help employees
    find information across company documentation. You will work
    with language models and semantic retrieval technologies.
    """
    
    job3 = """
    Join our innovative technology team where you'll help transform
    how our company works using cutting-edge artificial intelligence.
    """
    

    result = analyse_job_with_ai(job2)
    # print(result.model_dump())  # Print the structured analysis of the job description
    for key, value in result.model_dump().items():
        print(f"{key}: {value}")