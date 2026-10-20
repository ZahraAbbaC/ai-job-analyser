from typing import TypedDict, Any


class JobMatchState(TypedDict):
    job_description: str
    candidate_profile: dict[str, Any] | None
    job_preferences: dict[str, Any] | None
    skill_match: dict[str, Any] | None
    iterations: int
    status: str