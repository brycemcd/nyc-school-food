"""
Works similarly to a controller - handles skill request and provides response

Originally, this was boilerplate provided by AMZN
"""

from __future__ import print_function
from request import Request, ResponseBuilder


def skill_router(event):
    """Accepts the event being sent from the skill, gives it to the router and
       sends the response back to the skill
    """

    req = Request(event)
    resp = ResponseBuilder(req).resp
    return resp.return_resp()
