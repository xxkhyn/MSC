from collections import Counter
from types import SimpleNamespace
from MSC.logic.parser import parser, parse_def
from MSC.logic.yaku.judge_yaku import judge_yaku
from MSC.logic.yaku.yaku import calculate_waits
from MSC.models import Condition
from typing import Literal, Any
def classify_mentsu(m):
    if len(m) == 3:
        if m[0] + 1 == m[1] and m[1] + 1 == m[2]:
            return "shuntsu"
        elif m[0] == m[1] == m[2]:
            return "kotsu"
    return "unknown"



def run_full_flow(hand_pai, winning_pai, huuro=None,condition=None):
    huuro = huuro or []

    # 先に hand_obj を作る（hand_numeric はまだ無いので入れない）
    hand_obj = SimpleNamespace(
        hand_pai=hand_pai,
        winning_pai=winning_pai,
        huuro=huuro,
    )

    # hand_numeric を作成
    hand_numeric = parse_def.all_tiles_to_indices(hand_obj)

    # hand_numeric を hand_obj に追加（必要なら）
    hand_obj.hand_numeric = hand_numeric

    # tiles_count 作成
    tiles_count = [0] * 34
    count = Counter(hand_pai + [winning_pai])
    for tile_str, c in count.items():
        idx = parse_def.TILE_TO_NUMERIC[tile_str]  # 牌文字列→数値インデックス
        tiles_count[idx] = c

    # winning_tile_index
    winning_tile_index = parse_def.TILE_TO_NUMERIC[winning_pai]

    # analyze_hand_model は hand_obj 一つだけ引数
    result = parser.analyze_hand_model(hand_obj)

    first_pattern = result["agari_patterns"][0][0]  # 面子だけ
    pair = result["agari_patterns"][0][1]  # 雀頭


    # parsed_hand 辞書作成
    parsed_hand = {
    "hand_numeric": hand_numeric,
    "agari_patterns": result["agari_patterns"],
    "mentsu": [
        {"type": classify_mentsu(m), "tiles": m} for m in first_pattern
    ],
    "pair": {"tiles": pair},
    "melds": [],
    "huuro": huuro,
    "tiles_count": tiles_count,
    "winning_tile_index": winning_tile_index,
    "wait": calculate_waits(result)
}


    # 役判定
    yaku_result= judge_yaku(parsed_hand, huuro, condition)
    
    # 結果返却（必要に応じてyakuも返す）
    return {
        "agari_patterns": result["agari_patterns"],
        "melds": result["melds"],
        "melds_descriptions": result["melds_descriptions"],
        "error_message": result["error_message"],
        "yaku_result": yaku_result,
    }


if __name__ == "__main__":
    test_hand_pai = ["m1", "m1", "m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9", "m9", "m9"]
    test_winning_pai = "m5"
    test_huuro = []
    test_condition = Condition(
        is_riichi=False,
        is_double_riichi=False,
        is_ippatsu=False,
        is_rinshan=False,
        is_chankan=False,
        is_haitei=False,
        is_houtei=False,
        is_tenho=False,
        is_tsumo=True,
        seat_wind="east",

        prevalent_wind="east",
        player_type="child",
        kyotaku=0,
        honba=0,
    )

    result = run_full_flow(test_hand_pai, test_winning_pai, test_huuro, condition=test_condition)
    print(result)

    