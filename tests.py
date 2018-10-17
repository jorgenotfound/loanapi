from unittest import TestCase
import json
from http import HTTPStatus
from tornado.testing import AsyncHTTPTestCase
import app


class ValidateLoanTestCase(TestCase):

    def test_validate_loan_undecided(self):
        self.assertEqual(app.validate_loan(app.MAX_AMOUNT_ALLOWED), 'undecided')
        self.assertEqual(app.validate_loan(50000), 'undecided')
        self.assertEqual(app.validate_loan(3, 3), 'undecided')

    def test_validate_loan_approved(self):
        self.assertEqual(app.validate_loan(49999), 'approved')
        self.assertEqual(app.validate_loan(6, 7), 'approved')

    def test_validate_loan_declined(self):
        self.assertEqual(app.validate_loan(50001), 'declined')
        self.assertEqual(app.validate_loan(7, 6), 'declined')


class MainHandlerTestCase(AsyncHTTPTestCase):

    def get_app(self):
        return app.make_app()

    def test_main_handler(self):
        response = self.fetch('/')
        self.assertEqual(response.code, HTTPStatus.OK)
        self.assertEqual(response.body, b'Loan api')


class LoanHandlerTestCase(AsyncHTTPTestCase):

    def get_app(self):
        return app.make_app()

    def test_loan_handler_bad_request(self):
        data = {'bad': 'request'}
        response = self.fetch('/validate', body=json.dumps(data), method="POST")
        self.assertEqual(response.code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.body.decode(), 'Amount is required.')

    def test_loan_handler_undecided(self):
        data = {'amount': 50000}
        response = self.fetch('/validate', body=json.dumps(data), method="POST")
        self.assertEqual(response.code, HTTPStatus.OK)
        self.assertEqual(response.body.decode(), app.MESSAGES['undecided'])

    def test_loan_handler_approved(self):
        data = {'amount': 49999}
        response = self.fetch('/validate', body=json.dumps(data), method="POST")
        self.assertEqual(response.code, HTTPStatus.OK)
        self.assertEqual(response.body.decode(), app.MESSAGES['approved'])

    def test_loan_handler_declined(self):
        data = {'amount': 50001}
        response = self.fetch('/validate', body=json.dumps(data), method="POST")
        self.assertEqual(response.code, HTTPStatus.OK)
        self.assertEqual(response.body.decode(), app.MESSAGES['declined'])
