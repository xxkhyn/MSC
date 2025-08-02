from MSC.logic.parser.parse_def import TILE_TO_NUMERIC
TILE_TO_INDEX = TILE_TO_NUMERIC
from MSC.models import Condition
from MSC.logic.yaku.yaku import is_chiitoitsu
from MSC.logic.yaku.yaku import is_kokushi
from MSC.logic.yaku.yaku import is_kokushi_13machi
from MSC.logic.object.han import YakuCounter
from MSC.logic.object.han import Yakumann
from MSC.logic.parser.parse_def import tile_strs_to_indices
import math
yakuis_kokushi = is_kokushi
yakuis_kokushi_13machi = is_kokushi_13machi
yakuis_chiitoitsu = is_chiitoitsu
def calculate_fu(hand_instance, condition_instance, agari_pattern, yakuis_chiitoitsu,
                 yakuis_kokushi,yakuis_kokushi_13machi) -> int:
    mentsu_list, head = _normalize_mentsu_list(agari_pattern[0]), agari_pattern[1]
    winning_tile = TILE_TO_INDEX[hand_instance.winning_pai]

    # 七対子チェック（正しく counts34 相当のリストを作成）
    tile_indices = tile_strs_to_indices(hand_instance)
    counts = [tile_indices.count(i) for i in range(34)]
    if yakuis_chiitoitsu(counts, YakuCounter()):
        return 25

    #国士無双の場合、仮の符（３０）を返す
    if yakuis_kokushi(counts,Yakumann()):
        return 30
    if yakuis_kokushi_13machi(counts,winning_tile, Yakumann()):
        return 30
    
    # 門前平和ツモなら20符固定で終了
    if _is_pinfu(mentsu_list, head, winning_tile, hand_instance.is_huuro, hand_instance.is_tsumo):
        return 20
    
    # 初期符（門前ロンのみ30符、それ以外は20符）
    if not hand_instance.is_tsumo and not hand_instance.is_huuro:
        fu = 30  # 門前ロン
    else:
        fu = 20

    

    # 雀頭が役牌（自風・場風・三元牌）なら +2符
    if _is_yakuhai(head[0], condition_instance):
        fu += 2

    # 面子ごとの符
    for m in mentsu_list:
        tiles = m["tiles"]
        is_open = m["open"]
        tile = tiles[0]
        is_terminal_or_honor = tile >= 27 or tile % 9 in [0, 8]

        if len(tiles) == 3 and len(set(tiles)) == 1:  # 刻子
            fu += _calculate_kotsu_fu(is_open, is_terminal_or_honor)
        elif len(tiles) == 4:  # 槓子
            fu += _calculate_kan_fu(is_open, is_terminal_or_honor)

    # 門前ツモなら +2符（ただしピンフは除かれている）
    if hand_instance.is_tsumo and not hand_instance.is_huuro:
        fu += 2

    # 待ち形による +2符（単騎・カンチャン・ペンチャン）
    machi_type = get_machi_type(mentsu_list, head, winning_tile)
    if machi_type in ["tanki", "kanchan", "penchan"]:
        fu += 2

    return math.ceil(fu / 10) * 10


def _is_yakuhai(tile_index, condition):
    winds = ['east', 'south', 'west', 'north']
    try:
        seat_wind_idx = TILE_TO_INDEX[f"z{1 + winds.index(condition.seat_wind)}"]
        prevalent_wind_idx = TILE_TO_INDEX[f"z{1 + winds.index(condition.prevalent_wind)}"]
    except (KeyError, ValueError) as e:
        return False  # 風が不正な場合は無視

    yakuhai = {
        seat_wind_idx,
        prevalent_wind_idx,
        TILE_TO_INDEX["z5"], TILE_TO_INDEX["z6"], TILE_TO_INDEX["z7"]
    }
    return tile_index in yakuhai



def _normalize_mentsu_list(mentsu_list):
    """
    面子をすべて dict 型に正規化（tiles: List[int], open: bool）
    """
    normalized = []
    for m in mentsu_list:
        if not m:
            continue
        if isinstance(m, dict):
            normalized.append(m)
        else:
            normalized.append({"tiles": m, "open": False})
    return normalized


def _calculate_kotsu_fu(is_open, is_terminal_or_honor):
    if is_open:
        return 4 if is_terminal_or_honor else 2
    else:
        return 8 if is_terminal_or_honor else 4


def _calculate_kan_fu(is_open, is_terminal_or_honor):
    if is_open:
        return 16 if is_terminal_or_honor else 8
    else:
        return 32 if is_terminal_or_honor else 16


def get_machi_type(mentsu_list, head, winning_tile):
    # 単騎待ち
    if head[0] == winning_tile:
        return "tanki"

    for m in mentsu_list:
        tiles = m["tiles"]
        if winning_tile in tiles and len(tiles) == 3 and tiles[0] != tiles[1]:

            sorted_m = sorted(tiles)
            if sorted_m[1] == winning_tile:
                return "kanchan"
            elif sorted_m[0] == winning_tile and sorted_m[0] % 9 == 6:
                return "penchan"
            elif sorted_m[2] == winning_tile and sorted_m[2] % 9 == 2:
                return "penchan"
            else:
                return "ryanmen"

    return None # 刻子に当たった場合のシャンポンとみなす

def _is_pinfu(mentsu_list, head, winning_tile, is_huuro, is_tsumo):
    if is_huuro:
        return False
    if head[0] >= TILE_TO_INDEX["z1"]:  # 字牌の雀頭は役牌の可能性
        return False
    for m in mentsu_list:
        tiles = m["tiles"]
        if len(tiles) == 3 and len(set(tiles)) == 1:
            return False  # 刻子があるとピンフではない
    machi_type = get_machi_type(mentsu_list, head, winning_tile)
    return is_tsumo and machi_type == "ryanmen"