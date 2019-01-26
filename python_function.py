"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
from response import Response
from request import Request, ResponseBuilder
import datetime as dt
import menu as menu


# --------------- Functions that control the skill's behavior ------------------

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return Response.build_response({}, Response.build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def _food_for_date(meal, str_fx, date=None):
    """
    Returns the food being served for the specified meal on the specified date
    :param meal: A hash of date: food items (i.e. food.BREAKFAST)
    :param str_fx: A function that takes the result as an argument and returns a
        string for Echo to say
    :param date: string in Y-m-d format indicating date. Defaults to today()
    :return: string which will be Echo's response
    """

    if not date:
        # FIXME: this is in UTC!
        date = str(dt.date.today())

    date = dt.datetime.strptime(date, "%Y-%m-%d").date()
    day_str = date.strftime("%A")

    date = str(date)
    if day_str in ["Saturday", "Sunday"]:
        return "It is %s. No food is being served at school" % day_str
    elif menu.NO_SCHOOL_STRING in meal[date]:
        return "There is no school today"
    else:
        return str_fx(meal[date])


def breakfast_for_date(date=None):
    """Retrieve menu
    :param :date string in Y-m-d format representing date i.e. 2018-12-12
    """

    fx = lambda res: """
        On today's breakfast menu is %s. There will also be %s available.
    """ % (res[0], res[1])

    return _food_for_date(menu.BREAKFAST, fx, date)


def lunch_for_date(date=None):
    """Retrieve menu"""
    fx = lambda res: "On today's lunch menu is %s." % res

    return _food_for_date(menu.LUNCH, fx, date)


def get_breakfast(intent, session):
    """Fetch breakfast for the day"""

    session_attributes = {}
    card_title = "NYCSchool Food"
    # speech_output = """it is Saturday!"""
    speech_output = breakfast_for_date()

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = """Reprompting"""
    should_end_session = False
    return Response.build_response(session_attributes, Response.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_lunch(intent, session):
    """Fetch lunch for the day"""

    session_attributes = {}
    card_title = "NYCSchool Food"
    # speech_output = """it is Saturday!"""
    speech_output = lunch_for_date()

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = """Reprompting"""
    should_end_session = False
    return Response.build_response(session_attributes, Response.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# --------------- Events ------------------

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    # print("on_intent requestId=" + intent_request['requestId'] +
    #       ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "breakfast":
        return get_breakfast(intent, session)
    elif intent_name == "lunch":
        return get_lunch(intent, session)

    elif intent_name == "WhatsMyColorIntent":
        return get_color_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    # print("event.session.application.applicationId=" +
    #       event['session']['application']['applicationId'])

    req = Request(event)
    resp = ResponseBuilder(req).resp
    return resp.return_resp()


    if event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
