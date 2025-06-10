from msc_project.MSC.logic.object.han import Yakumann
from msc_project.MSC.logic.object.tiles import MahjongParser
from msc_project.MSC.models import ScoreResult

KOKUSHI_INDICES = [
    0, 8,        # 1m, 9m
    9, 17,       # 1p, 9p
    18, 26,      # 1s, 9s
    27, 28, 29, 30, 31, 32, 33  # 字牌
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


# --------------------------
# ScoreResult を使ってチェック
# --------------------------

# 例：最新のスコア結果を取得（適宜フィルタしてください）
result = ScoreResult.objects.latest('id')  # 例として最新のレコード

# 13枚の手牌（保存方法によって変わります、ここでは仮に渡されたとします）
# 例: tile_strs = ['m1', 'm9', ..., 'z7']
tile_strs = [...]  # ←ここに13枚をセット
winning_tile = result.winning_pai  # DBから取得

# 合成した14枚の牌を使って判定
full_tiles = tile_strs + [winning_tile]
tiles = MahjongParser.parse_tiles(full_tiles)
winning_tile_index = MahjongParser.parse_tiles([winning_tile]).index(1)

# 判定処理
yakuman_counter = Yakumann()

if is_kokushi(tiles):
    if is_kokushi_13machi(tiles, winning_tile_index):
        yakuman_counter.add_yaku("国士無双十三面待ち", 2)
    else:
        yakuman_counter.add_yaku("国士無双", 1)
