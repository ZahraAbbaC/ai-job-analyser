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
            call_id="call_123"
        )
    ],
    output_text=""
)


second_response = SimpleNamespace(
    status="completed",
    output=[
        SimpleNamespace(
            type="message",
            content=[]
        )
    ],
    output_text="The candidate is a strong match."
)


def test_match_job_passes_tool_result_back_to_model():
    with patch("src.job_matcher.client.responses.create") as mock_create:
        mock_create.side_effect = [first_response, second_response]

        result = match_job("Junior Backend Engineer requiring Python.")

    assert result == "The candidate is a strong match."
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

    assert function_call_output["call_id"] == "call_123"
    assert json.loads(function_call_output["output"]) == candidate_profile


def test_match_job_stops_after_max_iterations():
    with patch("src.job_matcher.client.responses.create") as mock_create:
        
        mock_create.return_value = first_response

        with pytest.raises(RuntimeError, match="Maximum iterations reached."):
            match_job("Junior Backend Engineer requiring Python.")
        
        assert mock_create.call_count == 5
