from django.test import TestCase
from MSC.logic.object.han import Yakumann
from MSC.logic.object.tiles import MahjongParser
from MSC.models import ScoreResult

KOKUSHI_INDICES = [
    0, 8,
    9, 17,
    18, 26,
    27, 28, 29, 30, 31, 32, 33
]

def is_kokushi(tiles):
    pair_count = 0
    for idx in KOKUSHI_INDICES:
        if tiles[idx] == 0:
            return False
        if tiles[idx] >= 2:
            pair_count += 1
    return pair_count == 1 and sum(tiles) == 14

def is_kokushi_13machi(tiles, winning_tile_index):
    return all(tiles[idx] == 1 for idx in KOKUSHI_INDICES) and winning_tile_index in KOKUSHI_INDICES


class KokushiTestCase(TestCase):
    def setUp(self):
        # 十三面待ち
        self.tiles_13machi = [
            'm1', 'm9',
            'p1', 'p9',
            's1', 's9',
            'z1', 'z2', 'z3', 'z4', 'z5', 'z6', 'z7'
        ]
        self.winning_tile_13 = 'z1'

        # 通常の国士無双（雀頭あり）
        self.tiles_normal = [
            'm1', 'm9',
            'p1', 'p9',
            's1', 's9',
            'z1', 'z2', 'z3', 'z4', 'z5', 'z6', 'z7', 'z1'  # z1 が2枚
        ]
        self.winning_tile_normal = 'z3'

    def test_kokushi_13machi(self):
        full_tiles = self.tiles_13machi + [self.winning_tile_13]
        tiles = MahjongParser.parse_tiles(full_tiles)
        winning_tile_index = MahjongParser.parse_tiles([self.winning_tile_13]).index(1)

        self.assertTrue(is_kokushi(tiles))
        self.assertTrue(is_kokushi_13machi(tiles, winning_tile_index))

        yakuman = Yakumann()
        if is_kokushi_13machi(tiles, winning_tile_index):
            yakuman.add_yaku("国士無双十三面待ち", 2)

        self.assertIn("国士無双十三面待ち", yakuman.get_yakus())
        self.assertEqual(yakuman.get_total(), 2)

    def test_kokushi_normal(self):
        tiles = MahjongParser.parse_tiles(self.tiles_normal)
        winning_tile_index = MahjongParser.parse_tiles([self.winning_tile_normal]).index(1)

        self.assertTrue(is_kokushi(tiles))
        self.assertFalse(is_kokushi_13machi(tiles, winning_tile_index))

        yakuman = Yakumann()
        if is_kokushi(tiles):
            yakuman.add_yaku("国士無双", 1)

        self.assertIn("国士無双", yakuman.get_yakus())
        self.assertEqual(yakuman.get_total(), 1)
