# MSC/tests/test_calculator.py

import pytest
from MSC.models import Hand, Condition
from MSC.logic import calculator

@pytest.mark.django_db
class TestCalculator:

    def test_kokushi_success(self):
        # 国士無双の必要牌 + ペア牌
        hand = Hand.objects.create(
            hand_pai=[
                '1m', '9m', '1p', '9p', '1s', '9s',
                'z1', 'z2', 'z3', 'z4', 'z5', 'z6', 'z7'
            ],
            winning_pai='z1',  # ペア完成
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

        # アサーション（期待結果）
        assert result.han == 13
        assert result.fu == 0
        assert result.point == 48000
        assert '国士無双' in result.yaku_list
        assert result.error_message == ""

    def test_kokushi_fail(self):
        # 国士無双になっていない手牌
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

        # アサーション（期待結果）
        assert result.han == 0
        assert result.point == 1000  # dummy_result() の point
        assert result.error_message == ""
