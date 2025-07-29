import unittest
from MSC.logic.score_calc_1.calculate_hu import calculate_fu
from MSC.logic.parser.parse_def import TILE_TO_NUMERIC
TILE_TO_INDEX = TILE_TO_NUMERIC


class MockHand:
    def __init__(self, winning_pai, is_tsumo=True, is_huuro=False, hand_pai=None, huuro=None):
        self.winning_pai = winning_pai
        self.is_tsumo = is_tsumo
        self.is_huuro = is_huuro
        self.hand_pai = hand_pai or []
        self.huuro = huuro or []


class MockCondition:
    def __init__(self, seat_wind='east', prevalent_wind='east'):
        self.seat_wind = seat_wind
        self.prevalent_wind = prevalent_wind


class TestFuCalculator(unittest.TestCase):

    def test_pinfu_tsumo(self):
        """門前平和ツモは常に20符"""
        hand = MockHand(
            winning_pai="m1",
            is_tsumo=True,
            is_huuro=False,
            hand_pai=["m1", "m2", "m3", "p4", "p5", "p6", "s6", "s7", "s8", "m7", "m8", "m9", "p3"]
        )
        condition = MockCondition()
        agari_pattern = (
            [
                {"tiles": [TILE_TO_INDEX["m1"], TILE_TO_INDEX["m2"], TILE_TO_INDEX["m3"]], "open": False},
                {"tiles": [TILE_TO_INDEX["p4"], TILE_TO_INDEX["p5"], TILE_TO_INDEX["p6"]], "open": False},
                {"tiles": [TILE_TO_INDEX["s6"], TILE_TO_INDEX["s7"], TILE_TO_INDEX["s8"]], "open": False},
                {"tiles": [TILE_TO_INDEX["m7"], TILE_TO_INDEX["m8"], TILE_TO_INDEX["m9"]], "open": False},
            ],
            [TILE_TO_INDEX["p3"]]
        )
        self.assertEqual(calculate_fu(hand, condition, agari_pattern, is_chiitoitsu = False), 20)

    def test_chiitoitsu(self):
        hand = MockHand(
            winning_pai="m3",
            is_tsumo=True,
            is_huuro=False,
            hand_pai=["m1", "m1", "p2", "p2", "s3", "s3", "m4", "m4", "p5", "p5", "s6", "s6", "m3"]
    )
        condition = MockCondition()
        agari_pattern = ([], [])
        self.assertEqual(calculate_fu(hand, condition, agari_pattern, is_chiitoitsu=True), 25)


    def test_ron_menzen_koutsu(self):
        """門前ロンで刻子あり + 役牌雀頭 + カンチャン待ち = 40符"""
        hand = MockHand(
            winning_pai="m3",
            is_tsumo=False,
            is_huuro=False,
            hand_pai=["m3", "m3", "p4", "p5", "p6", "s7", "s8", "s9", "m6", "m7", "m8", "z1", "z1"]
        )
        condition = MockCondition(seat_wind='east', prevalent_wind='south')
        agari_pattern = (
            [
                {"tiles": [TILE_TO_INDEX["m3"]] * 3, "open": False},
                {"tiles": [TILE_TO_INDEX["p4"], TILE_TO_INDEX["p5"], TILE_TO_INDEX["p6"]], "open": False},
                {"tiles": [TILE_TO_INDEX["s7"], TILE_TO_INDEX["s8"], TILE_TO_INDEX["s9"]], "open": False},
                {"tiles": [TILE_TO_INDEX["m6"], TILE_TO_INDEX["m7"], TILE_TO_INDEX["m8"]], "open": False},
            ],
            [TILE_TO_INDEX["z1"]]
        )
        self.assertEqual(calculate_fu(hand, condition, agari_pattern, is_chiitoitsu = False), 40)

    def test_ron_open_meld(self):
        """副露あり + 明刻中張子 + 役牌雀頭 + 単騎待ち = 40符"""
        hand = MockHand(
            winning_pai="m5",
            is_tsumo=False,
            is_huuro=True,
            hand_pai=["m5", "m5", "p2", "p3", "p4", "s6", "s7", "s8", "m7", "m8", "m9", "z5", "m5"],
            huuro=[{"type": "pon", "tiles": ["m5", "m5", "m5"], "open": True}]
        )
        condition = MockCondition()
        agari_pattern = (
            [
                {"tiles": [TILE_TO_INDEX["m5"]] * 3, "open": True},
                {"tiles": [TILE_TO_INDEX["p2"], TILE_TO_INDEX["p3"], TILE_TO_INDEX["p4"]], "open": False},
                {"tiles": [TILE_TO_INDEX["s6"], TILE_TO_INDEX["s7"], TILE_TO_INDEX["s8"]], "open": False},
                {"tiles": [TILE_TO_INDEX["m7"], TILE_TO_INDEX["m8"], TILE_TO_INDEX["m9"]], "open": False},
            ],
            [TILE_TO_INDEX["z5"]]
        )
        self.assertEqual(calculate_fu(hand, condition, agari_pattern, is_chiitoitsu = False), 40)


if __name__ == '__main__':
    unittest.main()
