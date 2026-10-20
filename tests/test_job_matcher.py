import pytest
import json
from types import SimpleNamespace
from unittest.mock import patch

from src.job_matcher import match_job
from src.tools import get_candidate_profile


first_response = SimpleNamespace(
    status="completed",
    output=[
        SimpleNamespace(
            type="function_call",
            name="get_candidate_profile",
            arguments="{}",
            call_id="call_1"
        )
    ],
    output_text=""
)

second_response = SimpleNamespace(
    status="completed",
    output=[
        SimpleNamespace(
            type="function_call",
            name="get_candidate_profile",
            arguments="{}",
            call_id="call_2"
        )
    ],
    output_text=""
)


last_response = SimpleNamespace(
    status="completed",
    output=[
        SimpleNamespace(
            type="message",
            content=[]
        )
    ],
    output_text="Job evaluation complete"
)


def test_match_job_passes_tool_result_back_to_model():
    with patch("src.job_matcher.client.responses.create") as mock_create:
        mock_create.side_effect = [first_response, last_response]

        result = match_job("Junior Backend Engineer requiring Python.")

    assert result == "Job evaluation complete"
    assert mock_create.call_count == 2

    second_call_input = mock_create.call_args_list[1].kwargs["input"]
    candidate_profile = get_candidate_profile()

    function_call_output = [
        item
        for item in second_call_input
        if isinstance(item, dict) and item.get("type") == "function_call_output"
    ]
    
    assert len(function_call_output) == 1 #verifies that the agent didn't send duplicate tool results
    
    function_call_output = function_call_output[0]

    assert function_call_output["call_id"] == "call_1"
    assert json.loads(function_call_output["output"]) == candidate_profile


def test_match_job_stops_after_max_iterations():
    with patch("src.job_matcher.client.responses.create") as mock_create:
        
        mock_create.return_value = first_response

        with pytest.raises(RuntimeError, match="Maximum iterations reached."):
            match_job("Junior Backend Engineer requiring Python.")
        
        assert mock_create.call_count == 5


def test_match_job_reuses_cached_candidate_profile():

    expected_profile = {
        "name": "Test Candidate",
        "skills": ["Python", "SQL"],
    }
    
    with patch("src.job_matcher.client.responses.create") as mock_create:
        with patch("src.job_matcher.execute_tool") as mock_execute:
            
            mock_create.side_effect = [first_response, second_response, last_response]
            mock_execute.return_value = expected_profile

            result = match_job("Junior Backend Engineer requiring Python.")

    assert result == "Job evaluation complete"
    assert mock_create.call_count == 3
    assert mock_execute.call_count == 1  # Ensures that the tool was only called once, demonstrating caching

    final_input = mock_create.call_args_list[2].kwargs["input"]

    function_outputs = [
        item
        for item in final_input
        if isinstance(item, dict) and item.get("type") == "function_call_output"
    ]

    assert len(function_outputs) == 2 # verifies that the agent sent exactly two tool outputs

    assert {item["call_id"] for item in function_outputs} == {"call_1", "call_2"} # verifies that the agent sent results associated with correct tool requests

    assert (
        json.loads(function_outputs[0]["output"]) 
        == json.loads(function_outputs[1]["output"])
    ) # verifies that both results contained identical data.

    assert json.loads(function_outputs[0]["output"]) == expected_profile # combined with the previous assertion, verifies that the cached result matches the expected candidate profile data.