import json
from openai import OpenAI
from dotenv import load_dotenv
from src.agent_state import JobMatchState
from src.tools import (
    candidate_profile_tool, 
    job_preferences_tool, 
    skill_match_tool, 
    execute_tool
)


load_dotenv()  # Load environment variables from .env file


client = OpenAI()  # Create an OpenAI client instance


def match_job(description: str):
    """
    Match a job description with a candidate's profile using OpenAI's Responses API.
    """

    state: JobMatchState = {
        "job_description": description,
        "candidate_profile": None,
        "job_preferences": None,
        "skill_match": None,
        "iterations": 0,
        "status": "running",
    }


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
        state["iterations"] += 1
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
            state["status"] = "completed"
            print("==== Final State ====,/n", state)
            return response.output_text  # return the final output text if no more tool calls are needed


        for item in tool_calls:
            print(f"Function call detected: {item.name}")
            print("arguments:", item.arguments)

            # cache tool outputs to avoid redundant calls and update the state accordingly
            if item.name == "get_candidate_profile" and state["candidate_profile"] is not None:
                tool_output = state["candidate_profile"]

            elif item.name == "get_job_preferences" and state["job_preferences"] is not None:
                tool_output = state["job_preferences"]

            else:
                tool_output = execute_tool(item.name, item.arguments)

                if item.name == "get_candidate_profile":
                    state["candidate_profile"] = tool_output

                elif item.name == "get_job_preferences":
                    state["job_preferences"] = tool_output

                elif item.name == "calculate_skill_match":
                    state["skill_match"] = tool_output


            input_list.append(
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(tool_output)
                }
            )

    state["status"] = "max_iterations_reached"
    raise RuntimeError("Maximum iterations reached.")    



jd1 = "We are looking for a Junior Backend Engineer. Required: Python, FastAPI, PostgreSQL, Docker. Experience with AWS is a plus."
jd2 = "Senior Data Engineer requiring Python, Spark, Airflow, AWS and Kubernetes." 
jd3 = "Join our innovative AI team to help improve internal business processes using emerging technologies."

if __name__ == "__main__":
    # match_job("Junior backend engineer requiring Python.")
    match_job(jd1)
    match_job(jd3)