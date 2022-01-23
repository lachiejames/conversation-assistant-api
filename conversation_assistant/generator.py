from conversation_assistant.gpt3 import fetch_completion
from conversation_assistant.models import (
    GPT3CompletionResponse,
    LambdaEvent,
    Suggestion,
)
from conversation_assistant.parsers import (
    map_completion_response_to_suggestions,
    map_messages_to_prompt,
)


def generate_message_suggestions(event: LambdaEvent):
    prompt: str = map_messages_to_prompt(event["previous_messages"])
    print(f"Constructed a prompt - {prompt}")

    completion_response: GPT3CompletionResponse = fetch_completion(prompt, event["gpt3_params"])
    print(f"Fetched GPT3 completion response - {completion_response}")

    suggestions: list[Suggestion] = map_completion_response_to_suggestions(completion_response)
    print(f"Generated suggestions - {suggestions}")

    return suggestions