from django.test import TestCase
from MSC.models import Hand, Condition
from MSC.logic import calculator

class CalculatorTest(TestCase):

    def test_kokushi_fail(self):
        hand = Hand.objects.create(
            hand_pai=[
                '1m', '2m', '3m', '4p', '5p', '6p',
                '7s', '8s', '9s', '1p', '2p', '3p', '4m'
            ],
            winning_pai='5p',
            is_huuro=False,
            huuro=[],
            dora_pai=[]
        )

        condition = Condition.objects.create(
            is_tsumo=True,
            is_riichi=False,
            prevalent_wind='east',
            seat_wind='south'
        )

        result = calculator.calculate_score(hand, condition)

        self.assertEqual(result.han, 0)
        self.assertEqual(result.point, 1000)
        self.assertEqual(result.error_message, "")
