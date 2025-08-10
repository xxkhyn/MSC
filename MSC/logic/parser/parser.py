from collections import Counter
from MSC.logic.object.han import Yakumann, YakuCounter
from MSC.logic.yaku.yaku import is_kokushi, is_kokushi_13machi, is_chiitoitsu
from . import parse_def
from MSC.logic.yaku.yaku import KOKUSHI_INDICES


def analyze_hand_model(hand_obj):
    aka_dora_count = 0

    # === 正規化 ===
    raw_tiles = hand_obj.hand_pai + [hand_obj.winning_pai]

    tiles_cleaned = []
    for tile in raw_tiles:
        if tile.endswith("'"):
            aka_dora_count += 1
            tile = tile[:-1]
        if len(tile) == 2 and tile[1] in "mps":
            tile = tile[1] + tile[0]
        tiles_cleaned.append(tile)

    # 副露も正規化
    for meld in hand_obj.huuro:
        new_tiles = []
        for t in meld["tiles"]:
            if len(t) == 2 and t[1] in "mps":
                t = t[1] + t[0]
            new_tiles.append(t)
        meld["tiles"] = new_tiles

    hand_obj.hand_pai = tiles_cleaned[:-1]
    hand_obj.winning_pai = tiles_cleaned[-1]

    # === 解析 ===
    hand_numeric = parse_def.tile_strs_to_indices(hand_obj)
    melds = parse_def.parse_huuro_to_melds(hand_obj)
    agari_patterns = parse_def.can_form_agari_numeric(hand_obj)

    yakumann = Yakumann()
    yakucounter = YakuCounter()

    # === 特殊役 ===
    chiitoi_result = is_chiitoitsu(tiles_cleaned, yakucounter)
    print("[DEBUG] 七対子判定:", chiitoi_result, "手牌:", tiles_cleaned)

    if not agari_patterns:
        tiles_count = [0] * 34
        for t in tiles_cleaned:
            idx = parse_def.TILE_TO_NUMERIC[t]
            tiles_count[idx] += 1
        winning_idx = parse_def.TILE_TO_NUMERIC[hand_obj.winning_pai]

        if is_kokushi_13machi(tiles_count, winning_idx, yakumann):
            kokushi_tiles = [parse_def.NUMERIC_TO_TILE[idx] for idx in KOKUSHI_INDICES]
            agari_patterns = []
            for tile_str in kokushi_tiles:
                agari_patterns.append(([[tile_str]], None))
            return {
                "kokushi_13machi": True,
                "agari_patterns": agari_patterns,
                "melds": [],
                "wait": kokushi_tiles,
                "melds_descriptions": [],
                "error_message": "",
                "aka_dora_count": aka_dora_count,
            }
        elif is_kokushi(tiles_cleaned, yakumann):
            kokushi_pattern = [[[parse_def.NUMERIC_TO_TILE[idx]] for idx in KOKUSHI_INDICES], None]
            agari_patterns = [kokushi_pattern]
            return {
                "kokushi": True,
                "agari_patterns": agari_patterns,
                "melds": [],
                "wait": [hand_obj.winning_pai],
                "melds_descriptions": [],
                "error_message": "",
                "aka_dora_count": aka_dora_count,
            }

        

        elif is_chiitoitsu(tiles_cleaned, yakucounter):
            counts = Counter(tiles_cleaned)
            pairs = []
            for tile, c in counts.items():
                if c == 2:
                    pairs.append([tile, tile])
            if pairs:
                # 七対子は雀頭を1つの対子として、残りの6つを面子扱いで返す
                pair = pairs[0]
                mentsu = pairs[1:]
                final_patterns = [(mentsu, pair)]
            else:
                final_patterns = []

            return {
                "chiitoitsu": True,
                "agari_patterns": final_patterns,
                "melds": [],
                "wait": [hand_obj.winning_pai],
                "melds_descriptions": ["七対子"],
                "error_message": "",
                "aka_dora_count": aka_dora_count,
            }
        

        
    # === 副露を agari_patterns に合体 ===
    final_patterns = []
    for pattern in agari_patterns:
        normal_mentsu, pair = pattern
        full_mentsu = normal_mentsu + [m for m in melds]
        final_patterns.append((full_mentsu, pair))

    # agari_patterns が空でも副露があれば最低限埋める
    if not agari_patterns and melds:
        final_patterns = [(melds, None)]

    print("[analyze_hand_model] final agari_patterns:", agari_patterns)

    return {
        "agari_patterns": final_patterns,
        "melds": melds,
        "melds_descriptions": [],
        "wait": [hand_obj.winning_pai],
        "error_message": "",
        "aka_dora_count": aka_dora_count,
    }
