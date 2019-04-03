"""
Handles voice responses in Alexa format
"""
import datetime as dt
import menu as menu


class Response:
    """Respond via voice"""

    def say(self):
        """Each child class should implement what to say"""
        raise NotImplementedError

    @property
    def should_end(self):
        """Each child class should implement what to say"""
        raise NotImplementedError

    @property
    def default_reprompt_text(self):
        return "Reprompting"

    def card(self):
        """Used on device to supplement voice response"""
        return {}

    def return_resp(self):
        """Stuff to return via voice and the cards"""

        return self.build_response(
                       self.build_speechlet_response(self.say(),
                                                     self.default_reprompt_text,
                                                     self.should_end,
                                                     self.card()))

    @staticmethod
    def build_speechlet_response(output, reprompt_text, should_end_session, card):
        return {
            'outputSpeech': {
                'type': 'PlainText',
                'text': output
            },
            # 'card': card,
            'reprompt': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': reprompt_text
                }
            },
            'shouldEndSession': should_end_session
        }

    @staticmethod
    def build_response(speechlet_response):
        return {
            'version': '1.0',
            'sessionAttributes': {},
            'response': speechlet_response
        }


class WelcomeResponse(Response):
    """Invoked when someone says something like 'open NYC school food'"""

    @property
    def should_end(self):
        return False

    def say(self):
        """What to say when entering the app"""
        return """Please say what is for the school meal"""


class GoodbyeResponse(Response):
    """Invoked when someone says something like 'open NYC school food'"""

    @property
    def should_end(self):
        return True

    def say(self):
        """What to say when entering the app"""
        return """Goodbye"""


class IntentResponse(Response):
    """Actually does stuff"""

    def __init__(self, date=None):
        if not date:
            # FIXME: this is in UTC!
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, "%Y-%m-%d").date()

    @property
    def should_end(self):
        return True

    def _food_for_date(self, meal, str_fx):
        """
        Returns the food being served for the specified meal on the specified date
        :param meal: A hash of date: food items (i.e. food.BREAKFAST)
        :param str_fx: A function that takes the result as an argument and returns a
            string for Echo to say
        :param date: string in Y-m-d format indicating date. Defaults to today()
        :return: string which will be Echo's response
        """

        day_str = self.date.strftime("%A")

        date_key = str(self.date)
        if day_str in ["Saturday", "Sunday"]:
            return "It is %s. No food is being served at school" % day_str
        elif menu.NO_SCHOOL_STRING in meal[date_key]:
            return "There is no school today"
        else:
            return str_fx(meal[date_key])

    def lunch_for_date(self):
        """Retrieve menu"""
        fx = lambda res: "On today's lunch menu is %s." % res

        return self._food_for_date(menu.LUNCH, fx)

    def breakfast_for_date(self):
        """Retrieve menu
        :param :date string in Y-m-d format representing date i.e. 2018-12-12
        """

        fx = lambda res: """
            On today's breakfast menu is %s. There will also be %s available.
        """ % (res[0], res[1])

        return self._food_for_date(menu.BREAKFAST, fx)

    def say(self):
        """What to say when entering the app"""
        resp = self.breakfast_for_date()
        resp += " "
        resp += self.lunch_for_date()
        return resp
