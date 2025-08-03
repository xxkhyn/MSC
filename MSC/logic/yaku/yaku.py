from MSC.logic.parser import parser
from MSC.logic.object.han import YakuCounter
from MSC.logic.object.han import Yakumann
from MSC.models import ScoreResult
from MSC import models
from typing import List


yakumann = Yakumann()
yakucounter = YakuCounter()
tile = models.Hand.hand_pai

from typing import List, Dict
from collections import Counter

# タイル番号辞書
TILE_TO_INDEX = {
    **{f"m{i}": i-1 for i in range(1, 10)},
    **{f"p{i}": 9 + i-1 for i in range(1, 10)},
    **{f"s{i}": 18 + i-1 for i in range(1, 10)},
    **{f"z{i}": 27 + i-1 for i in range(1, 8)},
}

NUMERIC_TO_TILE = {v: k for k, v in TILE_TO_INDEX.items()}

KOKUSHI_INDICES = [
    0, 8, 9, 17, 18, 26, 27, 28, 29, 30, 31, 32, 33
]


def calculate_waits(parsed_hand):
    # agari_patterns は複数の和了形候補
    waits = set()
    for pattern, wait_tiles in parsed_hand.get("agari_patterns", []):
        for w in wait_tiles:
            waits.add(w)
    return list(waits)



### === 役満 ===

def is_kokushi(tiles_str: list[str], yakumann: Yakumann) -> bool:
    terminals_and_honors = {'m1','m9','p1','p9','s1','s9',
                            'z1','z2','z3','z4','z5','z6','z7'}
    tile_set = set(tiles_str)
    if not terminals_and_honors.issubset(tile_set):
        return False
    counts = Counter(tiles_str)
    for t in terminals_and_honors:
        if counts[t] >= 2:
            yakumann.add_yaku("国士無双")
            return True
    return False


def is_kokushi_13machi(tiles: List[int], winning_tile_index: int, yakumann):
    for idx in KOKUSHI_INDICES:
        count = tiles[idx]
        if idx == winning_tile_index:
            # 和了牌は2枚までOK
            if count < 2:
                return False
        else:
            # 他は1枚のみ
            if count != 1:
                return False
    yakumann.add_yaku("国士無双十三面待ち")
    return True


def is_chinroutou(tiles: list[int], yakumann, huuro=None):
    # 字牌が混ざっていたらFalse
    if any(tiles[i] > 0 for i in range(27, 34)):
        return False

    # 数牌がすべて1か9かどうかチェック
    for i in range(27):
        if tiles[i] > 0:
            num = (i % 9) + 1
            if num not in (1, 9):
                return False

    yakumann.add_yaku("清老頭")
    return True

def is_tsuuiisou(tiles: List[int], yakumann, huuro=None):
    for i in range(27):
        if tiles[i] > 0:
            return False
    yakumann.add_yaku("字一色")
    return True

from collections import Counter

from collections import Counter

def is_chuuren(parsed_hand: dict, yakumann):

    tiles_flat = []
    for m in parsed_hand.get("mentsu", []):
        tiles = m.get("tiles", [])
    # もし tiles がリストのリストなら展開する
        for t in tiles:
            if isinstance(t, list):
                tiles_flat.extend(t)
            else:
                tiles_flat.append(t)

    pair_tiles = parsed_hand.get("pair", {}).get("tiles", [])
    for t in pair_tiles:
        if isinstance(t, list):
            tiles_flat.extend(t)
        else:
            tiles_flat.append(t)


    suits = set(idx // 9 for idx in tiles_flat)
    if len(suits) != 1:
        return False

    nums = [(idx % 9) + 1 for idx in tiles_flat]
    counter_tile = Counter(nums)

    base = [1,1,1,2,3,4,5,6,7,8,9,9,9]
    temp = counter_tile.copy()
    for n in base:
        if temp[n] == 0:
            return False
        temp[n] -= 1

    # 余りが winning tile と一致していれば純正
    winning_tile_index = parsed_hand.get("winning_tile_index")
    winning_num = (winning_tile_index % 9) + 1

    if sum(temp.values()) == 1 and temp[winning_num] == 1:
        yakumann.add_yaku("純正九蓮宝燈")
    else:
        yakumann.add_yaku("九蓮宝燈")

    return True


def is_ryuisou(parsed_hand: dict, yakumann, huuro=None):
    green = {"s2","s3","s4","s6","s8","z6"}
    for m in parsed_hand.get("mentsu", []) + [parsed_hand.get("pair")]:
        if m:
            tiles = [NUMERIC_TO_TILE[idx] for idx in m["tiles"]]
            if not all(t in green for t in tiles):
                return False
    yakumann.add_yaku("緑一色")
    return True

def is_daisuusii(parsed_hand: dict, yakumann, huuro=None):
    winds = {"z1","z2","z3","z4"}
    kotsu_count = 0
    for m in parsed_hand.get("mentsu", []):
        if m["type"] == "kotsu" and NUMERIC_TO_TILE[m["tiles"][0]] in winds:
            kotsu_count += 1
    if kotsu_count == 4:
        yakumann.add_yaku("大四喜")
    elif kotsu_count == 3 and NUMERIC_TO_TILE[parsed_hand["pair"]["tiles"][0]] in winds:
        yakumann.add_yaku("小四喜")
    else:
        return False
    return True

def is_sangenpai(parsed_hand: dict, yakumann, huuro=None):
    sangen = {"z5","z6","z7"}
    kotsu = [m for m in parsed_hand.get("mentsu", []) if m["type"] == "kotsu"]
    count = sum(1 for m in kotsu if NUMERIC_TO_TILE[m["tiles"][0]] in sangen)
    if count == 3:
        yakumann.add_yaku("大三元")
    elif count == 2:
        yakumann.add_yaku("小三元")
    else:
        return False
    return True

def is_suukantsu(parsed_hand: dict, yakumann, huuro=None):
    if sum(1 for m in parsed_hand.get("mentsu", []) if m["type"] == "kan") == 4:
        yakumann.add_yaku("四槓子")
        return True
    return False

def is_suuankou(parsed_hand: dict, yakumann, huuro=None):
    if sum(1 for m in parsed_hand.get("mentsu", []) if m["type"] == "kotsu" and not m.get("open", False)) == 4:
        yakumann.add_yaku("四暗刻")
        return True
    return False

def is_suuankou_tanki(parsed_hand: dict, yakumann, huuro=None):
    if sum(1 for m in parsed_hand.get("mentsu", []) if m["type"] == "kotsu" and not m.get("open", False)) == 4 and parsed_hand.get("wait") == "tanki":
        yakumann.add_yaku("四暗刻単騎")
        return True
    return False

### === 翻役 ===

def is_ryanpeikou(parsed_hand: dict, yaku_counter, huuro=None):
    if huuro: return False
    shuntsus = [tuple(sorted(m["tiles"])) for m in parsed_hand.get("mentsu", []) if m["type"] == "shuntsu"]
    pairs = []
    for i in range(len(shuntsus)):
        for j in range(i+1, len(shuntsus)):
            if shuntsus[i] == shuntsus[j]:
                pairs.append((i,j))
    if len(pairs) >= 2:
        yaku_counter.add_yaku("二盃口", 3)
        return True
    return False

def is_chiitoitsu(tiles_counts,yaku_counter):
    if len(tiles_counts) != 14:
        return False
    counts = Counter(tiles_counts)
    pairs = [c for c in counts.values() if c == 2]
    if len(pairs) == 7:
        yaku_counter.add_yaku("七対子", 2)
        return True
    return False


def is_ikkitsuukan(parsed_hand: dict, yaku_counter, huuro=None):
    suits = {"m":[False]*3, "p":[False]*3, "s":[False]*3}
    for m in parsed_hand.get("mentsu", []):
        if m["type"] == "shuntsu":
            idx = min(m["tiles"])
            tile = NUMERIC_TO_TILE[idx]
            suit, num = tile[0], int(tile[1])
            if num == 1: suits[suit][0] = True
            elif num == 4: suits[suit][1] = True
            elif num == 7: suits[suit][2] = True
    for k,v in suits.items():
        if all(v):
            yaku_counter.add_yaku("一気通貫", 1 if huuro else 2)
            return True
    return False

def is_sanshoku_doujun(parsed_hand: dict, yaku_counter, huuro=None):
    sequences = {}
    for m in parsed_hand.get("mentsu", []):
        if m["type"] == "shuntsu":
            idx = min(m["tiles"])
            tile = NUMERIC_TO_TILE[idx]
            suit, num = tile[0], int(tile[1])
            sequences.setdefault(num, set()).add(suit)
    if any(len(v) == 3 for v in sequences.values()):
        yaku_counter.add_yaku("三色同順", 1 if huuro else 2)
        return True
    return False
def is_sankantsu(parsed_hand: dict, yaku_counter, huuro=None):
    if sum(1 for m in parsed_hand.get("mentsu", []) if m["type"] == "kan") >= 3:
        yaku_counter.add_yaku("三槓子", 2)
        return True
    return False

def is_sanankou(parsed_hand: dict, yaku_counter, huuro=None):
    ankou = sum(1 for m in parsed_hand.get("mentsu", []) if m["type"] == "kotsu" and not m.get("open", False))
    if ankou >= 3:
        yaku_counter.add_yaku("三暗刻", 2)
        return True
    return False

def is_toitoi(parsed_hand: dict, yaku_counter, huuro=None):
    if all(m["type"] in {"kotsu", "kan"} for m in parsed_hand.get("mentsu", [])):
        yaku_counter.add_yaku("対々和", 2)
        return True
    return False

def is_honroutou(tiles: List[int], yaku_counter, huuro=None):
    for i in range(27):
        num = (i % 9) + 1
        if tiles[i] > 0 and num not in [1, 9]:
            return False
    yaku_counter.add_yaku("混老頭", 2)
    return True

def is_sanshoku_doukou(parsed_hand: dict, yaku_counter, huuro=None):
    counts = {}
    for m in parsed_hand.get("mentsu", []):
        if m["type"] == "kotsu":
            idx = m["tiles"][0]
            tile = NUMERIC_TO_TILE[idx]
            num = int(tile[1])
            suit = tile[0]
            counts.setdefault(num, set()).add(suit)
    if any(len(v) == 3 for v in counts.values()):
        yaku_counter.add_yaku("三色同刻", 2)
        return True
    return False

def is_tanyao(parsed_hand: dict, yaku_counter, huuro=None):
    for m in parsed_hand.get("mentsu", []) + [parsed_hand.get("pair")]:
        if not m: continue
        for idx in m["tiles"]:
            tile = NUMERIC_TO_TILE[idx]
            if tile.startswith("z") or tile[1] in {"1", "9"}:
                return False
    yaku_counter.add_yaku("断么九", 1)
    return True

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


def is_pinfu(parsed_hand, yaku_counter, huuro=None):
    mentsu_list = parsed_hand["mentsu"]
    head = parsed_hand["pair"]["tiles"]
    winning_tile = parsed_hand["winning_tile_index"]
    is_huuro_flag = len(huuro) > 0

    if is_huuro_flag:
        return False
    '''if head[0] >= TILE_TO_INDEX["z1"]:  # 字牌の雀頭は役牌の可能性
        return False'''
    if not head or len(head) ==0:
        return False
    for m in mentsu_list:
        tiles = m["tiles"]
        if len(tiles) == 3 and len(set(tiles)) == 1:
            return False  # 刻子があるとピンフではない
    # TODO: 待ち形チェックを適用するなら
    # machi_type = get_machi_type(mentsu_list, head, winning_tile)
    yaku_counter.add_yaku("ピンフ", 1)
    return True


def is_iipeikou(parsed_hand: dict, yaku_counter, huuro=None):
    if huuro: return False
    shuntsus = [tuple(sorted(m["tiles"])) for m in parsed_hand.get("mentsu", []) if m["type"] == "shuntsu"]
    for i in range(len(shuntsus)):
        for j in range(i + 1, len(shuntsus)):
            if shuntsus[i] == shuntsus[j]:
                yaku_counter.add_yaku("一盃口", 1)
                return True
    return False


def is_chanta(parsed_hand: dict, yaku_counter, huuro=None):
    """
    混全帯么（混全帯么）判定
    すべての面子に1・9牌または字牌が含まれていること
    """
    has_honor = False
    for m in parsed_hand.get("mentsu", []) + [parsed_hand.get("pair", {})]:
        tiles = m.get("tiles", [])
        # 面子・雀頭のどれかに必ず1・9・字牌が含まれるか判定
        if not any(
            NUMERIC_TO_TILE[t][0] == "z" or NUMERIC_TO_TILE[t][1] in {"1", "9"}
            for t in tiles
        ):
            return False
        if any(NUMERIC_TO_TILE[t][0] == "z" for t in tiles):
            has_honor = True

    if has_honor:
        yaku_counter.add_yaku("混全帯么", 2 if huuro else 3)
        return True
    return False

def is_junchan(parsed_hand: dict, yaku_counter, huuro=None):
    """
    純全帯么（ジュンチャン）判定
    混全帯么のうち字牌を含まない役
    """
    # まず混全帯么条件を満たしているか
    if not is_chanta(parsed_hand, yaku_counter=None):
        return False
    # 字牌を含むかチェック
    for m in parsed_hand.get("mentsu", []) + [parsed_hand.get("pair", {})]:
        tiles = m.get("tiles", [])
        if any(NUMERIC_TO_TILE[t][0] == "z" for t in tiles):
            return False  # 字牌含む → 純全帯么ではない

    yaku_counter.add_yaku("純全帯么", 3 if huuro else 6)
    return True


def resolve_conflicts(yaku_counter, yakumann):
    """
    両立できない役の競合を除去する。
    yakumann: Yakumann インスタンス
    yaku_counter: YakuCounter インスタンス
    """
    # 役満があれば通常役はすべて無効
    if yakumann.get_count() > 0:
        yaku_counter.clear()
        return

    # 平和と対々和は両立不可
    if "平和" in yaku_counter.get_yakus() and "対々和" in yaku_counter.get_yakus():
        yaku_counter.remove_yaku("対々和", 1)  # 平和優先

    # 七対子と二盃口は両立不可（ローカルルール次第）
    if "七対子" in yaku_counter.get_yakus() and "二盃口" in yaku_counter.get_yakus():
        yaku_counter.remove_yaku("七対子", 2)  # 二盃口の方が翻数高いので七対子を削除

    # 七対子と対々和は両立不可
    if "七対子" in yaku_counter.get_yakus() and "対々和" in yaku_counter.get_yakus():
        yaku_counter.remove_yaku("対々和", 2)

    # 七対子と三暗刻も同時成立しない
    if "七対子" in yaku_counter.get_yakus() and "三暗刻" in yaku_counter.get_yakus():
        yaku_counter.remove_yaku("三暗刻", 2)

    # 追加で他のルールがあればここに追記
