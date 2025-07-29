# test_fu_general.py

import pytest
from MSC.logic.score_calc_1.calculate_hu import calculate_fu
from MSC.logic.object.melds import TILE_TO_INDEX
from MSC.logic.yaku.yaku import is_chiitoitsu  # optional if chiitoitsu test used

# ---------- Dummy Classes ----------

class DummyHand:
    def __init__(self, winning_pai, is_tsumo, is_huuro):
        self.winning_pai = winning_pai
        self.is_tsumo = is_tsumo
        self.is_huuro = is_huuro

class DummyCondition:
    def __init__(self, seat_wind="east", prevalent_wind="east"):
        self.seat_wind = seat_wind
        self.prevalent_wind = prevalent_wind

# ---------- Helper Function ----------

def create_tile_list(tile_strs):
    return [TILE_TO_INDEX[tile] for tile in tile_strs]

# ---------- Main Test Function ----------

@pytest.mark.parametrize("description,expected_fu,yaku_name,machi_type,is_menzen,is_tsumo,winning_tile,mentsu_raw,head_raw", [
    # ピンフ ツモ リャンメン
    ("Pinfu Tsumo Ryanmen", 20, "pinfu", "ryanmen", True, True, "m2",
     [["m1", "m2", "m3"], ["p4", "p5", "p6"], ["s3", "s4", "s5"], ["s6", "s7", "s8"]],
     ["p2", "p2"]),
    
    # ピンフ不可：刻子あり＋タンキ
    ("No Pinfu - Koutsu + Tanki", 30, "none", "tanki", True, False, "z5",
     [["z5", "z5", "z5"], ["m2", "m3", "m4"], ["s2", "s3", "s4"], ["p7", "p8", "p9"]],
     ["z6", "z6"]),

    # 七対子は常に25符
    ("Chiitoitsu", 25, "chiitoitsu", "tanki", True, False, "z7",
     [],
     ["z1", "z1", "z2", "z2", "z3", "z3", "z4", "z4", "z5", "z5", "z6", "z6", "z7", "z7"]),

    # 明槓 vs 暗槓（中張牌）
    ("Open Kantsu - Chunchan", 50, "yakuhai", "tanki", False, False, "m5",
     [[{"tiles": ["m5", "m5", "m5", "m5"], "open": True}], ["s1", "s2", "s3"], ["p4", "p5", "p6"], ["z6", "z6", "z6"]],
     ["z5", "z5"]),

    ("Closed Kantsu - Chunchan", 70, "yakuhai", "tanki", True, False, "m5",
     [[{"tiles": ["m5", "m5", "m5", "m5"], "open": False}], ["s1", "s2", "s3"], ["p4", "p5", "p6"], ["z6", "z6", "z6"]],
     ["z5", "z5"]),

])
def test_calculate_fu(description, expected_fu, yaku_name, machi_type, is_menzen, is_tsumo, winning_tile, mentsu_raw, head_raw):
    # Setup hand and condition
    hand = DummyHand(winning_pai=winning_tile, is_tsumo=is_tsumo, is_huuro=not is_menzen)
    condition = DummyCondition()

    # Convert mentsu
    mentsu = []
    for m in mentsu_raw:
        if isinstance(m, dict) or (isinstance(m, list) and isinstance(m[0], dict)):
            # カン（明槓・暗槓）
            if isinstance(m, list) and isinstance(m[0], dict):
                m = m[0]
            tiles = create_tile_list(m["tiles"])
            mentsu.append({"tiles": tiles, "open": m["open"]})
        else:
            tiles = create_tile_list(m)
            mentsu.append(tiles)

    # Convert head
    head = create_tile_list(head_raw)

    # Prepare agari_pattern
    agari_pattern = [mentsu, head]

    # Calculate fu
    fu = calculate_fu(hand, condition, agari_pattern)

    assert fu == expected_fu, f"{description} → expected {expected_fu}, got {fu}"
