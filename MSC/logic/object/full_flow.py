from collections import Counter
from types import SimpleNamespace
from MSC.logic.parser import parser, parse_def
from MSC.logic.yaku.judge_yaku import judge_yaku
from MSC.logic.yaku.yaku import calculate_waits
from MSC.models import Condition,Hand
from MSC.logic.object.dora import count_dora

def classify_mentsu(m):
    if len(m) == 3:
        if m[0] + 1 == m[1] and m[1] + 1 == m[2]:
            return "shuntsu"
        elif m[0] == m[1] == m[2]:
            return "kotsu"
    return "unknown"

def run_full_flow(hand: Hand, condition: Condition = None):
    # hand.huuro は None かもしれないので空リストで補完
    huuro = hand.huuro or []

    # 解析用オブジェクト作成
    hand_obj = SimpleNamespace(
        hand_pai=hand.hand_pai,
        winning_pai=hand.winning_pai,
        huuro=huuro,
        dora_pai=getattr(hand, "dora_pai", [])  # dora_pai が Hand にあれば渡す
    )

    # 解析
    result = parser.analyze_hand_model(hand_obj)

    hand_numeric = parse_def.all_tiles_to_indices(hand_obj)
    hand_obj.hand_numeric = hand_numeric

    tiles_count = [0] * 34
    count = Counter(hand_obj.hand_pai + [hand_obj.winning_pai])
    for tile_str, c in count.items():
        idx = parse_def.TILE_TO_NUMERIC[tile_str]
        tiles_count[idx] = c

    winning_tile_index = parse_def.TILE_TO_NUMERIC[hand_obj.winning_pai]

    if result["agari_patterns"]:
        first_pattern = result["agari_patterns"][0]
        mentsu = first_pattern[0]
        pair = first_pattern[1]
    else:
        mentsu = []
        pair = []

    def flatten(lst):
        for item in lst:
            if isinstance(item, list):
                yield from flatten(item)
            else:
                yield item

    parsed_hand = {
        "hand_numeric": hand_numeric,
        "agari_patterns": result["agari_patterns"],
        "mentsu": [{"type": classify_mentsu(m), "tiles": list(flatten(m))} for m in mentsu],
        "pair": {"tiles": pair},
        "melds": [],
        "huuro": huuro,
        "tiles_count": tiles_count,
        "winning_tile_index": winning_tile_index,
        "wait": calculate_waits(result)
    }

    # 役判定
    yaku_result = judge_yaku(parsed_hand, huuro, condition)
    total_han = sum(yaku_result.values())

<<<<<<< Updated upstream
    # 通常ドラ
    if getattr(hand, "dora_pai", []):
        dora_count = count_dora(hand.hand_pai, hand.winning_pai, hand.dora_pai)
        total_han += dora_count
        if dora_count > 0:
            yaku_result["ドラ"] = dora_count

    # 赤ドラ
=======
    """if dora:
        dora_count = count_dora(hand_pai, winning_pai, dora)
        total_han += dora_count
        if dora_count > 0:
            yaku_result["ドラ"] = dora_count
"""
            
>>>>>>> Stashed changes
    aka_dora_count = result.get("aka_dora_count", 0)
    if aka_dora_count > 0:
        yaku_result["赤ドラ"] = aka_dora_count
        total_han += aka_dora_count

    return {
        "han": total_han,
        "yaku_list": yaku_result,
        "agari_patterns": result["agari_patterns"],
        "melds_descriptions": result["melds_descriptions"],
        "error_message": result["error_message"],
    }
