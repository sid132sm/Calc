from django.test import SimpleTestCase

from calculator.services.evaluator import ExpressionError, evaluate


class EvaluatorTests(SimpleTestCase):
    def test_respects_operator_precedence(self):
        self.assertEqual(evaluate("2+3×4"), "14")

    def test_supports_negative_numbers(self):
        self.assertEqual(evaluate("-8÷2"), "-4")

    def test_rejects_division_by_zero(self):
        with self.assertRaises(ExpressionError):
            evaluate("1÷0")

    def test_rejects_unknown_characters(self):
        with self.assertRaises(ExpressionError):
            evaluate("2+alert(1)")
