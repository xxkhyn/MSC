from collections import Counter
from types import SimpleNamespace
from MSC.logic.parser import parser, parse_def
from MSC.logic.yaku.judge_yaku import judge_yaku
from MSC.models import Condition, Hand
from MSC.logic.object.dora import count_dora


def classify_mentsu(m):
    if len(m) == 3:
        if m[0] + 1 == m[1] and m[1] + 1 == m[2]:
            return "shuntsu"
        elif m[0] == m[1] == m[2]:
            return "kotsu"
    elif len(m) == 4:
        return "kantsu"
    return "unknown"


def flatten_and_convert(lst):
    for item in lst:
        if isinstance(item, list):
            yield from flatten_and_convert(item)
        else:
            if isinstance(item, str):
                yield parse_def.TILE_TO_NUMERIC[item]
            else:
                yield item


def find_waiting_tiles(hand_obj, parser):
    waiting_tiles = set()
    all_tiles = list(parse_def.TILE_TO_NUMERIC.keys())

    for tile in all_tiles:
        test_hand = hand_obj.hand_pai + [tile]
        test_obj = SimpleNamespace(
            hand_pai=test_hand,
            winning_pai=tile,
            huuro=hand_obj.huuro,
            dora_pai=hand_obj.dora_pai
        )
        result = parser.analyze_hand_model(test_obj)

        if result.get("is_agari", False):
            waiting_tiles.add(tile)
        elif result.get("kokushi_13machi", False):
            waiting_tiles.add(tile)
        elif result.get("kokushi", False):
            waiting_tiles.add(tile)
        elif result.get("chiitoitsu", False):
            waiting_tiles.add(tile)
        elif result.get("agari_patterns"):
            waiting_tiles.add(tile)
        elif result.get("wait"):  # ← 追加。waitが空でなければ和了とみなす
            waiting_tiles.add(tile)

    return list(waiting_tiles)



def run_full_flow(hand: Hand, condition: Condition = None):
    huuro = hand.huuro or []

    hand_obj = SimpleNamespace(
        hand_pai=hand.hand_pai,
        winning_pai=hand.winning_pai,
        huuro=huuro,
        dora_pai=getattr(hand, "dora_pai", []),
    )

    # 解析実行
    result = parser.analyze_hand_model(hand_obj)

    # 待ち牌計算（resultにないか空の場合は自前計算）
    wait_tiles = result.get("wait")
    if not wait_tiles:
        wait_tiles = find_waiting_tiles(hand_obj, parser)
    result["wait"] = wait_tiles

    print("待ち牌:", result.get("wait"))

    # numeric に変換
    hand_numeric = parse_def.all_tiles_to_indices(hand_obj)
    hand_obj.hand_numeric = hand_numeric

    tiles_count = [0] * 34
    count = Counter(hand_obj.hand_pai + [hand_obj.winning_pai])
    for tile_str, c in count.items():
        idx = parse_def.TILE_TO_NUMERIC[tile_str]
        tiles_count[idx] = c

    winning_tile_index = parse_def.TILE_TO_NUMERIC[hand_obj.winning_pai]

    is_chiitoitsu = False
    is_kokushi = False
    mentsu, pair = [], []

    if result["agari_patterns"]:
        first_pattern = result["agari_patterns"][0]
        if len(first_pattern) == 2:
            if first_pattern[1] is None:
                is_chiitoitsu = True
                pair = []
                mentsu = first_pattern[0]
            else:
                mentsu = first_pattern[0]
                pair = first_pattern[1]
        elif "kokushi" in result or "kokushi_13machi" in result:
            is_kokushi = True
    else:
        return {
            "han": 0,
            "yaku_list": {},
            "agari_patterns": [],
            "melds_descriptions": [],
            "error_message": result.get("error_message", ""),
            "wait": [],
        }

    parsed_hand = {
        "hand_numeric": hand_numeric,
        "agari_patterns": result["agari_patterns"],
        "mentsu": [
            {"type": classify_mentsu(m), "tiles": list(flatten_and_convert(m))}
            for m in mentsu
        ] if mentsu else [],
        "pair": {"tiles": list(flatten_and_convert(pair))} if pair else {"tiles": []},
        "melds": [],
        "huuro": huuro,
        "tiles_count": tiles_count,
        "winning_tile_index": winning_tile_index,
        "wait": wait_tiles,
        "is_chiitoitsu": is_chiitoitsu,
        "is_kokushi": is_kokushi,
    }

    yaku_result = judge_yaku(parsed_hand, huuro, condition)
    total_han = sum(yaku_result.values())

    if getattr(hand, "dora_pai", []):
        dora_count = count_dora(hand.hand_pai, hand.winning_pai, hand.dora_pai)
        total_han += dora_count
        if dora_count > 0:
            yaku_result["ドラ"] = dora_count

    aka_dora_count = result.get("aka_dora_count", 0)
    if aka_dora_count > 0:
        yaku_result["赤ドラ"] = aka_dora_count
        total_han += aka_dora_count

    print("wait tiles:", wait_tiles)

    return {
        "han": total_han,
        "yaku_list": yaku_result,
        "agari_patterns": result["agari_patterns"],
        "melds_descriptions": result.get("melds_descriptions", []),
        "error_message": result.get("error_message", ""),
        "wait": wait_tiles,
    }
