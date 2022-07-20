from unittest.mock import MagicMock, patch

import pytest
from jsonschema import ValidationError

from ..gpt3 import fetch_completion, get_stop_indicator
from ..models import GPT3Params
from .mocks import (
    MOCK_GPT3_COMPLETION_RESPONSE,
    MOCK_PROMPT,
    MOCK_REQUEST,
    MOCK_STOP_INDICATOR,
)


def test_get_stop_indicator__returns_list_of_message_prefixes() -> None:
    stop_indicator = get_stop_indicator(request=MOCK_REQUEST)

    assert len(stop_indicator) == 2


@patch("conversation_assistant.gpt3.Completion.create", MagicMock(return_value=MOCK_GPT3_COMPLETION_RESPONSE))
def test_fetch_completion__when_gpt3_request_succeeds__then_returns_response() -> None:
    mock_gpt3_params: GPT3Params = MOCK_REQUEST["settings"]["gpt3_params"]

    response = fetch_completion(MOCK_PROMPT, mock_gpt3_params, MOCK_STOP_INDICATOR)

    assert response is MOCK_GPT3_COMPLETION_RESPONSE


@patch("conversation_assistant.gpt3.Completion.create", MagicMock(side_effect=LookupError))
def test_fetch_completion__when_gpt3_request_fails__then_raises_error() -> None:
    mock_gpt3_params: GPT3Params = MOCK_REQUEST["settings"]["gpt3_params"]

    with pytest.raises(LookupError):
        fetch_completion(MOCK_PROMPT, mock_gpt3_params, MOCK_STOP_INDICATOR)


@patch("conversation_assistant.gpt3.Completion.create", MagicMock(return_value={"this": "will fail"}))
def test_fetch_completion__when_gpt3_request_succeeds_but_validation_fails__then_raises_validation_error() -> None:
    mock_gpt3_params: GPT3Params = MOCK_REQUEST["settings"]["gpt3_params"]

    with pytest.raises(ValidationError):
        fetch_completion(MOCK_PROMPT, mock_gpt3_params, MOCK_STOP_INDICATOR)
