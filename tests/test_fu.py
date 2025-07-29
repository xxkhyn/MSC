import unittest
from MSC.logic.score_calc_1.calculate_hu import calculate_fu
from MSC.logic.object.melds import TILE_TO_INDEX


class MockHand:
    def __init__(self, winning_pai, is_tsumo=True, is_huuro=False):
        self.winning_pai = winning_pai
        self.is_tsumo = is_tsumo
        self.is_huuro = is_huuro


class MockCondition:
    def __init__(self, seat_wind='east', prevalent_wind='east'):
        self.seat_wind = seat_wind
        self.prevalent_wind = prevalent_wind


class TestFuCalculator(unittest.TestCase):

    def test_pinfu_tsumo(self):
        """門前平和ツモは常に20符"""
        hand = MockHand(winning_pai="3m", is_tsumo=True, is_huuro=False)
        condition = MockCondition()
        agari_pattern = (
            [
                {"tiles": [TILE_TO_INDEX["1m"], TILE_TO_INDEX["2m"], TILE_TO_INDEX["3m"]], "open": False},
                {"tiles": [TILE_TO_INDEX["4p"], TILE_TO_INDEX["5p"], TILE_TO_INDEX["6p"]], "open": False},
                {"tiles": [TILE_TO_INDEX["6s"], TILE_TO_INDEX["7s"], TILE_TO_INDEX["8s"]], "open": False},
                {"tiles": [TILE_TO_INDEX["7m"], TILE_TO_INDEX["8m"], TILE_TO_INDEX["9m"]], "open": False},
            ],
            [TILE_TO_INDEX["3p"]]  # 雀頭
        )
        self.assertEqual(calculate_fu(hand, condition, agari_pattern), 20)

    def test_chiitoitsu(self):
        """七対子は常に25符"""
        def is_chiitoitsu_mock(_, __): return True
        import MSC.logic.yaku.yaku
        MSC.logic.yaku.yaku.is_chiitoitsu = is_chiitoitsu_mock

        hand = MockHand(winning_pai="3m", is_tsumo=True, is_huuro=False)
        condition = MockCondition()
        agari_pattern = ([], [])  # 七対子は使わない
        self.assertEqual(calculate_fu(hand, condition, agari_pattern), 25)

    def test_ron_menzen_koutsu(self):
        """門前ロンで刻子あり、雀頭役牌、カンチャン待ち：例 30(初期) +2(役牌) +4(暗刻) +2(待ち) = 38 → 切り上げ40符"""
        hand = MockHand(winning_pai="3m", is_tsumo=False, is_huuro=False)
        condition = MockCondition(seat_wind='east', prevalent_wind='south')
        agari_pattern = (
            [
                {"tiles": [TILE_TO_INDEX["3m"], TILE_TO_INDEX["3m"], TILE_TO_INDEX["3m"]], "open": False},
                {"tiles": [TILE_TO_INDEX["4p"], TILE_TO_INDEX["5p"], TILE_TO_INDEX["6p"]], "open": False},
                {"tiles": [TILE_TO_INDEX["7s"], TILE_TO_INDEX["8s"], TILE_TO_INDEX["9s"]], "open": False},
                {"tiles": [TILE_TO_INDEX["2m"], TILE_TO_INDEX["3m"], TILE_TO_INDEX["4m"]], "open": False},
            ],
            [TILE_TO_INDEX["z1"]]  # 東が自風で役牌
        )
        self.assertEqual(calculate_fu(hand, condition, agari_pattern), 40)

    def test_ron_open_meld(self):
        """副露あり、ポン明刻、中張子、雀頭が役牌、単騎待ち：30(初期) +2(役牌) +2(明刻) +2(単騎) = 36 → 切り上げ40符"""
        hand = MockHand(winning_pai="5m", is_tsumo=False, is_huuro=True)
        condition = MockCondition()
        agari_pattern = (
            [
                {"tiles": [TILE_TO_INDEX["5m"], TILE_TO_INDEX["5m"], TILE_TO_INDEX["5m"]], "open": True},
                {"tiles": [TILE_TO_INDEX["2p"], TILE_TO_INDEX["3p"], TILE_TO_INDEX["4p"]], "open": False},
                {"tiles": [TILE_TO_INDEX["6s"], TILE_TO_INDEX["7s"], TILE_TO_INDEX["8s"]], "open": False},
                {"tiles": [TILE_TO_INDEX["7m"], TILE_TO_INDEX["8m"], TILE_TO_INDEX["9m"]], "open": False},
            ],
            [TILE_TO_INDEX["z5"]]  # 白
        )
        self.assertEqual(calculate_fu(hand, condition, agari_pattern), 40)


if __name__ == '__main__':
    unittest.main()
