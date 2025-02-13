import json
from unittest.mock import MagicMock, patch

from flask import Response
from jsonschema import ValidationError

from ..run import run_generate_suggestions
from .mocks import EMPTY_REQUEST, MOCK_RESPONSE


@patch("src.run.generate_suggestions", MagicMock(return_value=MOCK_RESPONSE))
def test_run_generate_suggestions__when_event_is_valid__then_response_code_is_200() -> None:
    response = run_generate_suggestions(EMPTY_REQUEST)

    assert response.status_code == 200


@patch("src.run.generate_suggestions", MagicMock(return_value=MOCK_RESPONSE))
def test_run_generate_suggestions__when_event_is_valid__then_returns_suggestions() -> None:
    response = run_generate_suggestions(EMPTY_REQUEST)

    assert response.data == json.dumps(MOCK_RESPONSE).encode()


@patch("src.run.validate_request", MagicMock(side_effect=ValidationError("test")))
def test_run_generate_suggestions__when_event_is_invalid__then_response_code_is_400() -> None:
    empty_event: dict[str, str] = {}
    response = run_generate_suggestions(empty_event)

    assert response.status_code == 400


@patch(
    "src.run.validate_request",
    MagicMock(side_effect=ValidationError("an error occurred")),
)
def test_run_generate_suggestions__when_event_is_invalid__then_returns_error_message() -> None:
    empty_event: dict[str, str] = {}
    response: Response = run_generate_suggestions(empty_event)

    assert response.data == b"an error occurred"


@patch("src.run.validate_request", MagicMock(side_effect=RuntimeError("an error occurred")))
def test_run_generate_suggestions__when_internal_error_raised__then_response_code_is_500() -> None:
    response: Response = run_generate_suggestions(EMPTY_REQUEST)
    assert response.status_code == 500


@patch("src.run.validate_request", MagicMock(side_effect=RuntimeError("an error occurred")))
def test_run_generate_suggestions__when_internal_error_raised__then_returns_error_message() -> None:
    response: Response = run_generate_suggestions(EMPTY_REQUEST)
    assert response.data == b"an error occurred"
