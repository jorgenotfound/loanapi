import os
import json
from http import HTTPStatus
import tornado.ioloop
import tornado.web

MESSAGES = {
    'undecided': 'The system cannot make a final decision about your loan.',
    'approved': 'Congratulations, your loan has been approved.',
    'declined': 'Your loan application has been declined.'
}
MAX_AMOUNT_ALLOWED = 50000


def validate_loan(requested_amount, max_allowed=MAX_AMOUNT_ALLOWED):
    """
    validate if a loan can be funded based on the requested amount

    :param requested_amount: int
    :param max_allowed: int
    :return: str
    """
    if requested_amount == max_allowed:
        return 'undecided'

    return 'approved' if requested_amount < max_allowed else 'declined'


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Loan api')


class LoanHandler(tornado.web.RequestHandler):

    def post(self):
        data = json.loads(self.request.body)

        try:
            status = HTTPStatus.OK
            response = MESSAGES[validate_loan(int(data['amount']))]
        except KeyError:
            status = HTTPStatus.BAD_REQUEST
            response = 'Amount is required.'
        finally:
            self.set_status(status)
            self.write(response)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/validate", LoanHandler),
    ], debug=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(int(os.environ.get('PORT', 8000)))
    tornado.ioloop.IOLoop.current().start()
