import json
from request import Request, ResponseBuilder
from response import WelcomeResponse, GoodbyeResponse, IntentResponse


def start_session_evt():
    """parsed start session as the lambda handler would see it"""
    j = open("json_responses/start_session_request.json", "r")
    return json.load(j)


def intent_evt():
    """parsed start session as the lambda handler would see it"""
    j = open("json_responses/lunch_intent_request.json", "r")
    return json.load(j)


def end_session_evt():
    """parsed start session as the lambda handler would see it"""
    j = open("json_responses/end_session_request.json", "r")
    return json.load(j)


def test_start_request_type():
    evt = start_session_evt()
    rqst = Request(evt)

    assert rqst.event_dict == evt
    assert rqst.request_type == "SessionStart"
    assert rqst.session_id == "amzn1.echo-api.session.123456789012"
    assert rqst.user_id == "amzn1.ask.account.testUser"
    assert rqst.intent_type is None
    assert type(rqst.intent_dict) == dict


def test_end_request_type():
    evt = end_session_evt()
    rqst = Request(evt)

    assert rqst.event_dict == evt
    assert rqst.request_type == "SessionEnd"
    assert rqst.session_id == "amzn1.echo-api.session.123456789012"
    assert rqst.user_id == "amzn1.ask.account.testUser"
    assert rqst.intent_type is None
    assert type(rqst.intent_dict) == dict


def test_intent_request_type():
    evt = intent_evt()
    rqst = Request(evt)

    assert rqst.event_dict == evt
    assert rqst.request_type == "Intent"
    assert rqst.session_id == "amzn1.echo-api.session.123456789012"
    assert rqst.user_id == "amzn1.ask.account.testUser"
    assert rqst.intent_type == "lunch"
    assert type(rqst.intent_dict) == dict


def test_response_builder():
    # Welcome Response
    rqst = Request(start_session_evt())
    resp_builder = ResponseBuilder(rqst)
    assert resp_builder.request_obj == rqst
    assert type(resp_builder.resp) == WelcomeResponse

    # Goodbye Request/Response
    rqst = Request(end_session_evt())
    resp_builder = ResponseBuilder(rqst)
    assert resp_builder.request_obj == rqst
    assert type(resp_builder.resp) == GoodbyeResponse

    # Intent Request/Response
    rqst = Request(intent_evt())
    resp_builder = ResponseBuilder(rqst)
    assert resp_builder.request_obj == rqst
    assert type(resp_builder.resp) == IntentResponse
