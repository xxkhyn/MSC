from msc_project.MSC.logic.object.han import Yakumann
from msc_project.MSC.logic.tiles import MahjongParser
from msc_project.MSC.models import ScoreResult


KOKUSHI_INDICES = [
    0, 8,       # 1m, 9m
    9, 17,      # 1p, 9p
    18, 26,     # 1s, 9s
    27, 28, 29, 30, 31, 32, 33  # 字牌
]


def is_kokushi(tiles):
    pair_count = 0
    for idx in KOKUSHI_INDICES:
        if tiles[idx] == 0:
            return False
        if tiles[idx] >= 2:
            pair_count += 1
    return pair_count == 1


# ここから処理
tiles = MahjongParser.parse_tiles(['m1', 'm9', '1', '1', '2', '3', '4', '5', '6', '7', 'p1', 'p9', 's1', 's9'])

yakuman_counter = Yakumann()

if is_kokushi(tiles):
    yakuman_counter.add_yaku("国士無双", 1) 
    
    ScoreResult.objects.create(
        yaku_list=list(yakuman_counter.get_yakus().keys()),
        han=yakuman_counter.get_total()
    )
