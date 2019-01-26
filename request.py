"""
Handles requests from voice
"""
from response import WelcomeResponse, GoodbyeResponse, IntentResponse


class ResponseBuilder:

    def __init__(self, request_obj):
        """
        Factory for building responses given a request obj
        :param request_obj: `Request` object
        :returns `Response` object
        """
        self.request_obj = request_obj
        if self.request_obj.request_type == "SessionStart":
            self.resp = WelcomeResponse()
        elif self.request_obj.request_type == "SessionEnd":
            self.resp = GoodbyeResponse()
        else:
            self.resp = IntentResponse()


class Request:
    """Handle requests made by voice"""

    def __init__(self, event_dict):
        self.event_dict = event_dict
        self.session_id = self.event_dict["session"]["sessionId"]
        self.user_id = self.event_dict["session"]["user"]["userId"]


    @property
    def request_type(self):
        """
        Returns string representation of request type.
        Valid values are:
            SessionStart (app opened)
            Intent
            SessionEnd
        """
        evt_request_type = self.event_dict["request"]["type"]
        hsh_map = {
            "LaunchRequest": "SessionStart",
            "SessionEndedRequest": "SessionEnd",
            "IntentRequest": "Intent"

        }
        return hsh_map[evt_request_type]

    @property
    def intent_type(self):
        if self.request_type != "Intent":
            return None
        else:
            return self.event_dict["request"]["intent"]["name"]

    @property
    def intent_dict(self):
        if self.request_type != "Intent":
            return {}
        else:
            return self.event_dict["request"]["intent"]
