from msc_project.MSC.logic.object import tiles
from msc_project.MSC.logic.object.han import YakuCounter
from msc_project.MSC.logic.object.tiles import MahjongParser
from msc_project.MSC.models import ScoreResult


def is_chiitoitsu(tiles):
    """
    七対子判定関数
    34種の牌枚数リスト tiles を受け取り、
    七対子なら True, それ以外は False を返す
    """
    if sum(tiles) != 14:
        return False

    pair_count = 0
    for count in tiles:
        if count == 2:
            pair_count += 1
        elif count != 0:
            return False

    return pair_count == 7

yaku_counter = YakuCounter()
if is_chiitoitsu(tiles):
    yaku_counter.add_yaku("七対子", 2)  # 翻数はルールに合わせて調整
