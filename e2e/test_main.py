import json
import os
from typing import Any, List
import unittest
import unittest.mock
from conversation_assistant.models import GenerateMessageSuggestionsRequest, LambdaResponse, Suggestion
from conversation_assistant.test.mocks import MOCK_REQUEST, MOCK_SUGGESTIONS

from main import generate_suggestions


def test_generate_suggestions__when_valid_request_received__then_returns_1_suggestion():
    path_to_schema: str = os.path.join("events", "tinder.json")
    with open(path_to_schema, "r", encoding="utf-8") as schema_file:
        request: GenerateMessageSuggestionsRequest = json.load(schema_file)

        response: LambdaResponse = generate_suggestions(request)
        parsed_response: Any = json.loads(response["body"])
        suggestions: List[Suggestion] = parsed_response["results"]

        assert len(suggestions) == 1
