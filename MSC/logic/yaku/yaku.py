from logic.object import tiles
from logic.object.han import YakuCounter
from logic.object.han import Yakumann
from logic.object.tiles import MahjongParser
from models import ScoreResult
from logic.object import melds
from MSC import models

KOKUSHI_INDICES = [
    0, 8,   # m1, m9
    9, 17,  # p1, p9
    18, 26, # s1, s9
    27, 28, 29, 30, 31, 32, 33  # 字牌
]

# ✅ 役満

def is_kokushi(tiles, YakuCounter):
    pair_count = 0
    for idx in KOKUSHI_INDICES:
        if tiles[idx] == 0:
            return False
        if tiles[idx] >= 2:
            pair_count += 1
    if pair_count == 1 and sum(tiles) == 14:
        YakuCounter.add_yaku("国士無双", 1, is_yakuman=True)
        return True
    return False

def is_kokushi_13machi(tiles, winning_tile_index, YakuCounter):
    if all(tiles[idx] == 1 for idx in KOKUSHI_INDICES) and winning_tile_index in KOKUSHI_INDICES:
        YakuCounter.add_yaku("国士無双十三面待ち", 2, is_yakuman=True)
        return True
    return False

def is_chinroutou(tiles, YakuCounter):
    for i in range(0, 27):
        num = i % 9 + 1
        if tiles[i] > 0 and num != 1 and num != 9:
            return False
    YakuCounter.add_yaku("清老頭", 1, is_yakuman=True)
    return True

def is_tsuuiisou(tiles, YakuCounter):
    for i in range(27):
        if tiles[i] > 0:
            return False
    YakuCounter.add_yaku("字一色", 1, is_yakuman=True)
    return True

def is_chuuren(parsed_hand, YakuCounter):
    from collections import Counter
    tiles_flat = []
    for m in parsed_hand.get("mentsu", []) + [parsed_hand.get("pair", {})]:
        tiles_flat.extend(m.get("tiles", []))
    suits = {t[1] for t in tiles_flat if not t.startswith("z")}
    if len(suits) != 1:
        return False
    nums = [int(t[0]) for t in tiles_flat if not t.startswith("z")]
    counter_tile = Counter(nums)
    base = [1,1,1,2,3,4,5,6,7,8,9,9,9]
    for i in base:
        if counter_tile[i] == 0:
            return False
    YakuCounter.add_yaku("九蓮宝燈", 1, is_yakuman=True)
    return True

def is_ryuisou(parsed_hand, YakuCounter):
    green_tiles = {"s2", "s3", "s4", "s6", "s8", "z6"}
    for m in parsed_hand.get("mentsu", []) + [parsed_hand.get("pair", {})]:
        if not all(t in green_tiles for t in m.get("tiles", [])):
            return False
    YakuCounter.add_yaku("緑一色", 1, is_yakuman=True)
    return True

def is_daisuusii(parsed_hand, YakuCounter):
    winds = {"z1", "z2", "z3", "z4"}
    count = 0
    for m in parsed_hand.get("mentsu", []):
        if m["type"] == "kotsu" and m["tiles"][0] in winds:
            count += 1
    if count == 4:
        YakuCounter.add_yaku("大四喜", 1, is_yakuman=True)
        return True
    elif count == 3:
        pair_tile = parsed_hand.get("pair", {}).get("tiles", [None])[0]
        if pair_tile in winds:
            YakuCounter.add_yaku("小四喜", 1, is_yakuman=True)
            return True
    return False

def is_sangenpai(parsed_hand, YakuCounter):
    sangen = {"z5": "白", "z6": "發", "z7": "中"}
    count = 0
    for m in parsed_hand.get("mentsu", []):
        if m["type"] == "kotsu" and m["tiles"][0] in sangen:
            count += 1
    if count == 2:
        YakuCounter.add_yaku("小三元", 2)
        return True
    elif count == 3:
        YakuCounter.add_yaku("大三元", 1, is_yakuman=True)
        return True
    return False

def is_suukantsu(parsed_hand, YakuCounter):
    kan_count = sum(1 for m in parsed_hand.get("mentsu", []) if m["type"] == "kan")
    if kan_count == 4:
        YakuCounter.add_yaku("四槓子", 1, is_yakuman=True)
        return True
    return False

def is_suuankou(parsed_hand, YakuCounter):
    ankou_count = sum(1 for m in parsed_hand.get("mentsu", []) if m["type"] == "kotsu" and not m.get("open", False))
    if ankou_count == 4:
        YakuCounter.add_yaku("四暗刻", 1, is_yakuman=True)
        return True
    return False

def is_suuankou_tanki(parsed_hand, YakuCounter):
    ankou_count = sum(1 for m in parsed_hand.get("mentsu", []) if m["type"] == "kotsu" and not m.get("open", False))
    if ankou_count == 4 and parsed_hand.get("wait") == "tanki":
        YakuCounter.add_yaku("四暗刻単騎", 2, is_yakuman=True)
        return True
    return False

def is_chinitsu(parsed_hand, YakuCounter, huuro):
    suits = set()
    for m in parsed_hand.get("mentsu", []) + [parsed_hand.get("pair", {})]:
        for tile in m.get("tiles", []):
            if tile.startswith("z"):
                return False
            suits.add(tile[1])
    if len(suits) == 1:
        YakuCounter.add_yaku("清一色", 5 if huuro else 6)
        return True
    return False

def is_honitsu(parsed_hand, YakuCounter, huuro):
    suits = set()
    has_honor = False
    for m in parsed_hand.get("mentsu", []) + [parsed_hand.get("pair", {})]:
        for tile in m.get("tiles", []):
            if tile.startswith("z"):
                has_honor = True
            else:
                suits.add(tile[1])
    if has_honor and len(suits) == 1:
        YakuCounter.add_yaku("混一色", 2 if huuro else 3)
        return True
    return False

"""3翻"""

def is_ryanpeikou(parsed_hand, YakuCounter, huuro):
    if huuro:
        return False
    shuntsus = [tuple(m["tiles"]) for m in parsed_hand.get("mentsu", []) if m["type"] == "shuntsu"]
    used = set()
    pair_count = 0
    for i in range(len(shuntsus)):
        for j in range(i+1, len(shuntsus)):
            if shuntsus[i] == shuntsus[j] and (i,j) not in used and (j,i) not in used:
                pair_count += 1
                used.add((i,j))
                break
    if pair_count == 2:
        YakuCounter.add_yaku("二盃口", 3)
        return True
    return False

# ✅ 2翻

def is_chiitoitsu(tiles, YakuCounter):
    pair_count = 0
    for count in tiles:
        if count == 2:
            pair_count += 1
        elif count != 0:
            return False
    if pair_count == 7:
        YakuCounter.add_yaku("七対子", 2)
        return True
    return False

def is_ikkitsuukan(parsed_hand, YakuCounter, huuro):
    is_huuro = bool(huuro)
    suits = {"m": [False]*3, "p": [False]*3, "s": [False]*3}
    for m in parsed_hand.get("mentsu", []):
        if m["type"] == "shuntsu":
            base = m["tiles"][0]
            num = int(base[0])
            suit = base[1]
            if num == 1:
                suits[suit][0] = True
            elif num == 4:
                suits[suit][1] = True
            elif num == 7:
                suits[suit][2] = True
    for suit in suits:
        if all(suits[suit]):
            YakuCounter.add_yaku("一気通貫", 1 if is_huuro else 2)
            return True
    return False

def is_sanshoku_doujun(parsed_hand, YakuCounter, huuro):
    is_huuro = bool(huuro)
    sequences = {}
    for m in parsed_hand.get("mentsu", []):
        if m["type"] == "shuntsu":
            base = m["tiles"][0]
            num = int(base[0])
            suit = base[1]
            sequences.setdefault(num, set()).add(suit)
    for suits in sequences.values():
        if len(suits) == 3:
            YakuCounter.add_yaku("三色同順", 1 if is_huuro else 2)
            return True
    return False

def is_sankantsu(parsed_hand, YakuCounter, huuro):
    kan_count = sum(1 for m in parsed_hand.get("mentsu", []) if m["type"] == "kan")
    if kan_count >= 3:
        YakuCounter.add_yaku("三槓子", 2)
        return True
    return False

def is_sanankou(parsed_hand, YakuCounter):
    ankou_count = 0
    for meld in parsed_hand.get("mentsu", []):
        if meld["type"] == "kotsu" and not meld.get("open", False):
            ankou_count += 1
    if ankou_count >= 3:
        YakuCounter.add_yaku("三暗刻", 2)
        return True
    return False

def is_toitoi(parsed_hand, YakuCounter):
    for m in parsed_hand.get("mentsu", []):
        if m["type"] != "kotsu" and m["type"] != "kan":
            return False
    YakuCounter.add_yaku("対々和", 2)
    return True

def is_honroutou(tiles, YakuCounter):
    for i in range(0, 27):
        num = i % 9 + 1
        if tiles[i] > 0 and num != 1 and num != 9:
            return False
    YakuCounter.add_yaku("混老頭", 2)
    return True

def is_sanshoku_doukou(parsed_hand, YakuCounter, huuro):
    counts = {}
    for m in parsed_hand.get("mentsu", []):
        if m["type"] == "kotsu":
            base = m["tiles"][0]
            num = int(base[0])
            suit = base[1]
            counts.setdefault(num, set()).add(suit)
    for suits in counts.values():
        if len(suits) == 3:
            YakuCounter.add_yaku("三色同刻", 2)
            return True
    return False

# ✅ 1翻

def is_tanyao(parsed_hand, YakuCounter, huuro):
    for m in parsed_hand.get("mentsu", []) + [parsed_hand.get("pair", {})]:
        for tile in m.get("tiles", []):
            if tile.startswith("z") or tile[0] in ["1", "9"]:
                return False
    YakuCounter.add_yaku("断么九", 1)
    return True

def is_pinfu(parsed_hand, YakuCounter, huuro):
    if huuro:
        return False
    if parsed_hand.get("pair", {}).get("type") == "honor":
        return False
    for m in parsed_hand.get("mentsu", []):
        if m["type"] != "shuntsu":
            return False
    if parsed_hand.get("wait") != "ryanmen":
        return False
    YakuCounter.add_yaku("平和", 1)
    return True

def is_iipeikou(parsed_hand, YakuCounter, huuro):
    if huuro:
        return False
    shuntsus = [tuple(m["tiles"]) for m in parsed_hand.get("mentsu", []) if m["type"] == "shuntsu"]
    for i in range(len(shuntsus)):
        for j in range(i + 1, len(shuntsus)):
            if shuntsus[i] == shuntsus[j]:
                YakuCounter.add_yaku("一盃口", 1)
                return True
    return False

def resolve_conflicts(self):
    # 複合不可の役の排他制御例
    if "四暗刻単騎" in self.yaku and "四暗刻" in self.yaku:
        self.remove_yaku("四暗刻")  # 上位役を優先
    if "小三元" in self.yaku and "大三元" in self.yaku:
        self.remove_yaku("小三元")
    if "二盃口" in self.yaku and "一盃口" in self.yaku:
        self.remove_yaku("一盃口")