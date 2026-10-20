import json


def get_candidate_profile():
    return {
        "name": "Candidate number one",
        "skills": [
            "Python",
            "SQL",
            "PostgreSQL",
            "FastAPI",
            "Docker",
        ],
    }


candidate_profile_tool = {
    "type": "function",
    "name": "get_candidate_profile",
    "description": (
        "Get the candidate's profile, including their name and technical skills. "
        "Use this when candidate information is needed to evaluate a job match."
    ),
    "parameters": {
        "type": "object",
        "properties": {},
        "additionalProperties": False,
    },
    "strict": True,
}


def get_job_preferences():
    return {
        "preferred_seniority": ["Junior", "Entry Level"],
        "preferred_roles": [
            "AI Engineer",
            "Backend Engineer",
            "AI Automation Engineer",
        ],
        "remote_ok": True,
    }


job_preferences_tool = {
    "type": "function",
    "name": "get_job_preferences",
    "description": (
        "Get the candidate's job preferences, including preferred seniority, roles, and remote work options. "
        "Use this when evaluating job matches based on candidate preferences."
    ),
    "parameters": {
        "type": "object",
        "properties": {},
        "additionalProperties": False,
    },
    "strict": True,
}


def calculate_skill_match(required_skills, candidate_skills):
    
    required_skills = {skill.strip().lower() for skill in required_skills}
    candidate_skills = {skill.strip().lower() for skill in candidate_skills}


    matched_skills = required_skills & candidate_skills  # Intersection of required and candidate skills
    missing_skills = required_skills - candidate_skills  # Skills required but not possessed by the candidate
    
    
    if not required_skills:
        match_percentage = 100  # If no required skills, consider it a perfect match
    elif not candidate_skills:
        match_percentage = 0  # If candidate has no skills, consider it a complete mismatch
    else:
        match_percentage = (len(matched_skills) / len(required_skills)) * 100 
    
    
    match_result = {
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),
        "match_percentage": match_percentage
    }


    return match_result


skill_match_tool = {
    "type": "function",
    "name": "calculate_skill_match",
    "description": (
        "Calculate the match percentage between required skills and candidate skills. "
        "Use this when evaluating how well a candidate's skills align with job requirements."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "required_skills": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of skills required for the job."
            },
            "candidate_skills": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of skills the candidate possesses."
            }
        },
        "required": ["required_skills", "candidate_skills"],
        "additionalProperties": False,
    },
    "strict": True,
}


#TODO: replace with tool registry later to avoid hardcoding tool names in execute_tool 
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

