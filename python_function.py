"""
Works similarly to a controller - handles skill request and provides response

Originally, this was boilerplate provided by AMZN
"""

from __future__ import print_function
from request import Request, ResponseBuilder


# NOTE: context is a required param for Lambda though it's not used in this app
def skill_router(event, context=None):
    """Accepts the event being sent from the skill, gives it to the router and
       sends the response back to the skill
    """

    req = Request(event)
    resp = ResponseBuilder(req).resp
    return resp.return_resp()
