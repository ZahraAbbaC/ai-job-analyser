import json
from openai import OpenAI
from src.tools import candidate_profile_tool, get_candidate_profile, job_preferences_tool, get_job_preferences, skill_match_tool, calculate_skill_match
from dotenv import load_dotenv


load_dotenv()  # Load environment variables from .env file


client = OpenAI()  # Create an OpenAI client instance


def execute_tool(name: str, arguments: str):
    args = json.loads(arguments)

    if name == "get_candidate_profile":
        return get_candidate_profile()
    elif name == "get_job_preferences":
        return get_job_preferences()
    elif name == "calculate_skill_match":
        return calculate_skill_match(args['required_skills'], args['candidate_skills'])
    else:
        raise ValueError(f"Unknown tool : {name}")


def match_job(description: str):
    """
    Match a job description with a candidate's profile using OpenAI's Responses API.
    """


    instructions = (
        "Evaluate whether the job matches the candidate. "
        "Use the tools to retrieve candidate information and preferences. "
        "Use calculate_skill_match to calculate the exact skill match score. "
        "Clearly distinguish required-skill coverage from overall job suitability. "
        "If the job description has no explicit required skills, "
        "do not present a 100% score as evidence of a perfect match. "
        "Do not invent candidate skills. Do not invent job requirements. "
    )


    input_list = [{"role": "user", "content": description}]
    
    
    tools = [candidate_profile_tool, job_preferences_tool, skill_match_tool]


    max_iterations = 5

    for iteration in range(max_iterations):
        print(f"\n--- Iteration {iteration + 1} ---")

        response = client.responses.create(
            model = "gpt-4o-mini",
            instructions = instructions,
            input = input_list,
            tools = tools
        )


        input_list.extend(response.output)


        tool_calls = [item for item in response.output if item.type == "function_call"]


        if not tool_calls:
            if response.status != "completed":
                raise RuntimeError(
                    f"Model response did not complete: {response.status}"
                )
            return response.output_text  # return the final output text if no more tool calls are needed


        for item in tool_calls:
            print(f"Function call detected: {item.name}")
            print("arguments:", item.arguments)
            tool_output = execute_tool(item.name, item.arguments)
            input_list.append(
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(tool_output)
                }
            )

    raise RuntimeError("Maximum iterations reached.")    



jd1 = "We are looking for a Junior Backend Engineer. Required: Python, FastAPI, PostgreSQL, Docker. Experience with AWS is a plus."
jd2 = "Senior Data Engineer requiring Python, Spark, Airflow, AWS and Kubernetes." 
jd3 = "Join our innovative AI team to help improve internal business processes using emerging technologies."
print(match_job(jd2))