import python_function as pf
import pytest
from test_request import start_session_evt
import json


def start_session_evt():
    """parsed start session as the lambda handler would see it"""
    j = open("json_responses/start_session_request.json", "r")
    return json.load(j)


def end_session_evt():
    """parsed start session as the lambda handler would see it"""
    j = open("json_responses/end_session_request.json", "r")
    return json.load(j)


def intent_evt():
    """parsed start session as the lambda handler would see it"""
    j = open("json_responses/lunch_intent_request.json", "r")
    return json.load(j)


def has_reqd_keys(resp):
    """tests that response dict has all the keys needed"""
    reqd_keys = {'response', 'version', 'sessionAttributes'}
    resp_keys = set(resp.keys())

    keys = (reqd_keys.difference(resp_keys))

    if keys:
        pytest.fail(f"required keys are missing from the response: {keys}")
    else:
        return True


def has_reqd_speechlet_keys(resp):
    """tests that response dict has all the keys needed"""
    reqd_keys = {'outputSpeech', 'reprompt', 'shouldEndSession'}
    resp_keys = set(resp['response'].keys())

    keys = (reqd_keys.difference(resp_keys))

    if keys:
        pytest.fail(f"required keys are missing from the response: {keys}")
    else:
        return True


# NOTE: these are designed to be more like integration tests than unit tests

def test_lambda_handler_welcome():

    evt_dict = start_session_evt()
    resp = pf.skill_router(evt_dict)

    has_reqd_keys(resp)
    has_reqd_speechlet_keys(resp)
    assert resp['response']['shouldEndSession'] is False


def test_lambda_handler_goodbye():

    evt_dict = end_session_evt()
    resp = pf.skill_router(evt_dict)

    has_reqd_keys(resp)
    has_reqd_speechlet_keys(resp)
    assert resp['response']['shouldEndSession'] is True


def test_skill_router_intent():

    evt_dict = intent_evt()
    resp = pf.skill_router(evt_dict)

    has_reqd_keys(resp)
    has_reqd_speechlet_keys(resp)
    assert resp['response']['shouldEndSession'] is True
