from response import Response, WelcomeResponse, GoodbyeResponse, IntentResponse
from unittest import mock


def test_response_return_resp():
    # using WelcomeResponse as a generic response to test parent class attribs
    wel = WelcomeResponse()

    ret_resp = wel.return_resp()

    assert type(ret_resp) == dict

    reqd_keys = ["version", "sessionAttributes", "response"]
    for key in reqd_keys:
        assert key in ret_resp.keys()

    # version is always 1.0
    assert ret_resp['version'] == '1.0'
    # we don't use session data in this app
    assert ret_resp['sessionAttributes'] == {}


def test_build_speechlet_response():
    resp = Response.build_speechlet_response("foo", "something Alexa says", "reprompt", True)

    assert type(resp["card"]) == dict
    assert type(resp["shouldEndSession"]) == bool

    acceptable_root_keys = ['card', 'outputSpeech', 'reprompt', 'shouldEndSession']
    for k in resp.keys():
        assert k in acceptable_root_keys


def test_welcome_response():
    welcome_response = WelcomeResponse()

    assert "Please say" in welcome_response.say()
    assert welcome_response.should_end is False


def test_goodbye_response():
    gb_response = GoodbyeResponse()

    assert "Goodbye" in gb_response.say()
    assert gb_response.should_end is True


def test_lunch_intent_response():

    # Weekday case
    weekday_date = "2018-12-20"
    with mock.patch("menu.LUNCH", {"2018-12-20": "Pizza"}):
        with mock.patch("menu.BREAKFAST", {"2018-12-20": "Pizza"}):
            lunch_response = IntentResponse(date=weekday_date)
            res = lunch_response.say()

            assert "today's lunch menu" in res
            assert "Pizza" in res
            assert "lunch menu" in lunch_response.say()

    # Weekend case
    weekend_date = "2018-12-22"
    lunch_response = IntentResponse(date=weekend_date)
    res = lunch_response.say()

    assert "No food is being served" in res
    assert lunch_response.should_end is True


def test_bkfast_for_date():
    # Weekday case

    weekday_date = "2018-12-20"
    with mock.patch("menu.BREAKFAST", {"2018-12-20": "Pizza"}):
        with mock.patch("menu.LUNCH", {"2018-12-20": "Pizza"}):
            bkfst_response = IntentResponse(date=weekday_date)
            res = bkfst_response.say()

            assert "today's lunch menu" in res
            assert "Pizza" in res

    # Weekend case
    weekend_date = "2018-12-22"
    bkfst_response = IntentResponse(date=weekend_date)
    res = bkfst_response.say()

    assert "No food is being served" in res
    assert bkfst_response.should_end is True
