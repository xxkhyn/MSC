from collections import Counter
from types import SimpleNamespace
from MSC.logic.parser import parser, parse_def
from MSC.logic.yaku.judge_yaku import judge_yaku
from MSC.models import Condition, Hand
from MSC.logic.object.dora import count_dora


def classify_mentsu(m):
    print(f"[classify_mentsu] raw input: {m}")

    if isinstance(m, dict):
        print("[classify_mentsu] already dict, return type:", m.get("type"))
        return m.get("type", "unknown")

    if len(m) == 3:
        m_sorted = sorted(m)
        print(f"[classify_mentsu] sorted: {m_sorted}")
        if m_sorted[0] + 1 == m_sorted[1] and m_sorted[1] + 1 == m_sorted[2]:
            print("[classify_mentsu] -> SHUNTSU")
            return "shuntsu"
        elif m_sorted[0] == m_sorted[1] == m_sorted[2]:
            print("[classify_mentsu] -> KOTSU")
            return "kotsu"
    elif len(m) == 4:
        print("[classify_mentsu] -> KAN")
        return "kan"

    print("[classify_mentsu] -> UNKNOWN")
    return "unknown"



def flatten_and_convert(lst):
    for item in lst:
        if isinstance(item, list):
            yield from flatten_and_convert(item)
        else:
            print(f"[flatten_and_convert] item: {item}")
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

    # === 解析実行 ===
    result = parser.analyze_hand_model(hand_obj)

    # 待ち牌計算
    wait_tiles = result.get("wait") or find_waiting_tiles(hand_obj, parser)
    result["wait"] = wait_tiles

    print("待ち牌:", wait_tiles)

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
    mentsu = []
    pair = []

    

    # === 面子構築 ===
    print("[run_full_flow] raw agari_patterns:", result["agari_patterns"])
    parsed_mentsu = []
    for m in mentsu:
        print("[run_full_flow] raw mentsu item:", m)
        if isinstance(m, dict):
            parsed_mentsu.append(m)
        elif isinstance(m, list):
            m_flat = list(flatten_and_convert(m))
            print("[run_full_flow] flat converted:", m_flat)
            parsed_mentsu.append({
                "type": classify_mentsu(m_flat),
                "tiles": m_flat
            })
        else:
            print(f"[run_full_flow] Unknown mentsu type: {m}")

# === agari_patterns でパターン決定 ===
    if result["agari_patterns"]:
        agari_patterns = result["agari_patterns"]
        final_pattern = agari_patterns[0]

        for pattern in agari_patterns:
            test_mentsu, test_pair = pattern
            kotsu_count = 0
            for m in test_mentsu:
                m_type = classify_mentsu(m)
                if m_type == "kotsu":
                    kotsu_count += 1
            if kotsu_count == 4:
                final_pattern = pattern
                print("[選択] 四暗刻候補パターン採用")
                break

        mentsu, pair = final_pattern

        # チートイツか国士は別扱い
        if "kokushi" in result or "kokushi_13machi" in result:
            is_kokushi = True
        if pair is None:
            is_chiitoitsu = True

        # === 面子解析 ===
        parsed_mentsu = []
        for m in mentsu:
            if isinstance(m, dict):
                parsed_mentsu.append(m)
            elif isinstance(m, list):
                m_flat = list(flatten_and_convert(m))
                parsed_mentsu.append({
                    "type": classify_mentsu(m_flat),
                    "tiles": m_flat
                })

        parsed_pair = {"tiles": list(flatten_and_convert(pair))} if pair else {"tiles": []}

        parsed_hand = {
            "hand_numeric": hand_numeric,
            "agari_patterns": result["agari_patterns"],
            "mentsu": parsed_mentsu,
            "pair": parsed_pair,
            "melds": huuro,
            "huuro": huuro,
            "tiles_count": tiles_count,
            "winning_tile_index": winning_tile_index,
            "wait": wait_tiles,
            "is_chiitoitsu": is_chiitoitsu,
            "is_kokushi": is_kokushi,
        }

        # === 単騎待ちチェック ===
        if pair and len(pair) == 2 and pair[0] == pair[1]:
            if pair[0] == winning_tile_index:
                parsed_hand["wait"] = "tanki"

    else:
        return {
            "han": 0,
            "yaku_list": {},
            "agari_patterns": [],
            "melds_descriptions": result.get("melds_descriptions", []),
            "error_message": result.get("error_message", ""),
            "wait": [],
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

    print("役:", yaku_result)

    return {
        "han": total_han,
        "yaku_list": yaku_result,
        "agari_patterns": result["agari_patterns"],
        "melds_descriptions": result.get("melds_descriptions", []),
        "error_message": result.get("error_message", ""),
        "wait": wait_tiles,
    }
