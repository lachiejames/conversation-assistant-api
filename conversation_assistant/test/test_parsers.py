from conversation_assistant.models import Message, Suggestion
from conversation_assistant.parsers import (
    map_completion_response_to_suggestions,
    map_messages_to_prompt,
)
from conversation_assistant.test.mocks import (
    MOCK_COMPLETION_RESPONSE,
    MOCK_MESSAGES,
    MOCK_PROMPT,
    MOCK_SUGGESTIONS,
)


def test_map_completion_response_to_suggestions_returns_expected_suggestions():
    suggestions: list[Suggestion] = map_completion_response_to_suggestions(MOCK_COMPLETION_RESPONSE)

    assert suggestions == MOCK_SUGGESTIONS


def test_map_messages_to_prompt_concatenates_author_with_text():
    prompt: list[Message] = map_messages_to_prompt(MOCK_MESSAGES)

    assert prompt == MOCK_PROMPT
