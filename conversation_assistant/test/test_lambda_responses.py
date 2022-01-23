from pytest_mock import MockerFixture

import conversation_assistant.generator
from conversation_assistant.lambda_helper import lambda_response
from conversation_assistant.models import LambdaResponse
from conversation_assistant.test.mocks import MOCK_LAMBDA_EVENT


def test_lambda_response__when_event_is_valid__then_response_code_is_200():
    response = lambda_response(MOCK_LAMBDA_EVENT)

    assert response["statusCode"] == 200


def test_lambda_response__when_event_is_valid__then_returns_at_least_1_message_suggestion():
    response: LambdaResponse = lambda_response(MOCK_LAMBDA_EVENT)

    assert len(response["body"]["results"]) > 0


def test_lambda_response__when_event_is_invalid__then_response_code_is_400():
    response = lambda_response({})

    assert response["statusCode"] == 400


def test_lambda_response__when_event_is_invalid__then_returns_error_message():
    empty_event = {}
    response: LambdaResponse = lambda_response(empty_event)

    assert response["body"] == "Error - Invalid event\n" + "error='body' is a required property"


def test_lambda_response__when_internal_error_raised__then_response_code_is_500(mocker: MockerFixture):
    mocker.patch.object(conversation_assistant.generator, "generate_message_suggestions", side_effect=RuntimeError("fake error"))

    response: LambdaResponse = lambda_response(MOCK_LAMBDA_EVENT)
    assert response["statusCode"] == 500


def test_lambda_response__when_internal_error_raised__then_returns_error_message(mocker: MockerFixture):
    mocker.patch.object(conversation_assistant.generator, "generate_message_suggestions", side_effect=RuntimeError("fake error"))

    response: LambdaResponse = lambda_response(MOCK_LAMBDA_EVENT)
    assert response["body"] == "Error - Something went wrong"