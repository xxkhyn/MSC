# judge_yaku.py

from collections import Counter
from MSC.logic.object.han import Yakumann, YakuCounter
from MSC.models import Condition

from MSC.logic.yaku.yaku import (
    is_kokushi, is_kokushi_13machi, is_chinroutou, is_tsuuiisou,
    is_chuuren, is_ryuisou, is_daisuusii, is_sangenpai,
    is_suukantsu, is_suuankou, is_suuankou_tanki,
    is_ryanpeikou, is_chiitoitsu, is_ikkitsuukan, is_sanshoku_doujun,
    is_sankantsu, is_sanankou, is_toitoi, is_honroutou,
    is_sanshoku_doukou, is_tanyao, is_pinfu, is_iipeikou,
    resolve_conflicts
)


# judge_yaku.py の先頭あたりに置くのがベストです。

CONFLICT_RULES = {
    "四暗刻単騎": ["四暗刻"],
    "大四喜": ["小四喜"],
    "国士無双十三面待ち": ["国士無双"],
    "七対子": [
        "一盃口", "対々和", "三暗刻", "三槓子", "三色同順", "三色同刻",
        "一気通貫", "混全帯么", "純全帯么", "平和"
    ],
    "二盃口": ["一盃口", "七対子"],
    "対々和": ["三暗刻"],
    "平和": ["対々和", "三暗刻", "一盃口", "混全帯么", "純全帯么"],
    "混全帯么": ["断么九"],
    "純全帯么": ["断么九"],
    "清一色": ["混一色"],
    "混一色": ["清一色"],
}


NUMERIC_TO_TILE = {
    0: "m1", 1: "m2", 2: "m3", 3: "m4", 4: "m5", 5: "m6", 6: "m7", 7: "m8", 8: "m9",
    9: "p1", 10: "p2", 11: "p3", 12: "p4", 13: "p5", 14: "p6", 15: "p7", 16: "p8", 17: "p9",
    18: "s1", 19: "s2", 20: "s3", 21: "s4", 22: "s5", 23: "s6", 24: "s7", 25: "s8", 26: "s9",
    27: "z1", 28: "z2", 29: "z3", 30: "z4", 31: "z5", 32: "z6", 33: "z7",
}

def tiles_count_to_tiles_str(tiles_counts):
    tiles_str = []
    for i, c in enumerate(tiles_counts):
        tiles_str.extend([NUMERIC_TO_TILE[i]] * c)
    return tiles_str

def wind_to_tile(wind_str: str) -> str:
    return {"east": "z1", "south": "z2", "west": "z3", "north": "z4"}.get(wind_str, "z1")

def judge_condition_yaku(parsed_hand, yaku_counter, condition: Condition):
    seat_wind_tile = wind_to_tile(condition.seat_wind)
    prevalent_wind_tile = wind_to_tile(condition.prevalent_wind)

    if condition.is_double_riichi:
        yaku_counter.remove_yaku("リーチ")
    if condition.is_ippatsu:
        yaku_counter.add_yaku("一発", 1)
    if condition.is_rinshan:
        yaku_counter.add_yaku("嶺上開花", 1)
    if condition.is_chankan:
        yaku_counter.add_yaku("槍槓", 1)
    if condition.is_haitei:
        yaku_counter.add_yaku("海底摸月", 1)
    if condition.is_houtei:
        yaku_counter.add_yaku("河底撈魚", 1)
    if condition.is_tenho:
        yaku_counter.add_yaku("天和", 1)
    if condition.is_tsumo:
        yaku_counter.add_yaku("ツモ", 1)

    for meld in parsed_hand.get("mentsu", []):
        if meld["type"] in ("kotsu", "kan"):
            tile_idx = meld["tiles"][0]
            tile_str = NUMERIC_TO_TILE[tile_idx]
            if tile_str.startswith("z"):
                if tile_str == seat_wind_tile:
                    yaku_counter.add_yaku("自風牌", 1)
                if tile_str == prevalent_wind_tile:
                    yaku_counter.add_yaku("場風牌", 1)
                if tile_str in {"z5", "z6", "z7"}:
                    yaku_counter.add_yaku("三元牌", 1)

# === ここから重複除去 ===
priority = {
    "国士無双十三面待ち": 2,
    "国士無双": 1,
}

def normalize(yaku_name):
    return yaku_name.strip()

def similar(yaku1, yaku2):
    pairs = [("国士無双十三面待ち", "国士無双")]
    y1 = normalize(yaku1)
    y2 = normalize(yaku2)
    return (y1, y2) in pairs or (y2, y1) in pairs

def remove_similar_duplicates(yaku_dict):
    print("重複除去前:", yaku_dict)
    items = sorted(yaku_dict.items(), key=lambda x: priority.get(x[0], 0), reverse=True)
    result = {}
    for yaku, han in items:
        if any(similar(yaku, other) for other in result):
            print(f"重複スキップ: {yaku}")
            continue
        result[yaku] = han
    yaku_dict.clear()
    yaku_dict.update(result)
    print("重複除去後:", yaku_dict)
    return result

# === メイン ===
def judge_yaku(parsed_hand, huuro=None, condition=None):
    yakumann = Yakumann()
    yaku_counter = YakuCounter()

    tiles_counts = parsed_hand.get("tiles_count")
    winning_tile_index = parsed_hand.get("winning_tile_index")

    if not parsed_hand.get("mentsu") and not parsed_hand.get("pair"):
        if tiles_counts:
            tiles_str = tiles_count_to_tiles_str(tiles_counts)
            is_kokushi(tiles_str, yakumann)
            if winning_tile_index is not None:
                is_kokushi_13machi(tiles_counts, winning_tile_index, yakumann)
            is_chinroutou(tiles_counts, yakumann)
            is_tsuuiisou(tiles_counts, yakumann)
        if yakumann.get_count() > 0:
            remove_similar_duplicates(yakumann.get_yakus())
            return yakumann.get_yakus()
        return {}

    if tiles_counts:
        tiles_str = tiles_count_to_tiles_str(tiles_counts)
        is_kokushi(tiles_str, yakumann)
        if winning_tile_index is not None:
            is_kokushi_13machi(tiles_counts, winning_tile_index, yakumann)
        is_chinroutou(tiles_counts, yakumann)
        is_tsuuiisou(tiles_counts, yakumann)

    is_chuuren(parsed_hand, yakumann)
    is_ryuisou(parsed_hand, yakumann)
    is_daisuusii(parsed_hand, yakumann)
    is_sangenpai(parsed_hand, yakumann)
    is_suukantsu(parsed_hand, yakumann)
    is_suuankou(parsed_hand, yakumann)
    is_suuankou_tanki(parsed_hand, yakumann)

    if yakumann.get_count() > 0:
        remove_similar_duplicates(yakumann.get_yakus())
        return yakumann.get_yakus()

    is_ryanpeikou(parsed_hand, yaku_counter, huuro)
    is_chiitoitsu(tiles_counts, yaku_counter)
    is_ikkitsuukan(parsed_hand, yaku_counter, huuro)
    is_sanshoku_doujun(parsed_hand, yaku_counter, huuro)
    is_sankantsu(parsed_hand, yaku_counter, huuro)
    is_sanankou(parsed_hand, yaku_counter)
    is_toitoi(parsed_hand, yaku_counter)
    is_honroutou(tiles_counts, yaku_counter)
    is_sanshoku_doukou(parsed_hand, yaku_counter, huuro)
    is_tanyao(parsed_hand, yaku_counter, huuro)
    is_pinfu(parsed_hand, yaku_counter, huuro)
    is_iipeikou(parsed_hand, yaku_counter, huuro)

    resolve_conflicts(yaku_counter, yakumann)

    if yakumann.get_count() == 0 and condition:
        judge_condition_yaku(parsed_hand, yaku_counter, condition)

    if yakumann.get_count() > 0:
        remove_similar_duplicates(yakumann.get_yakus())
        return yakumann.get_yakus()
    else:
        remove_similar_duplicates(yaku_counter.get_yakus())
        return yaku_counter.get_yakus()
