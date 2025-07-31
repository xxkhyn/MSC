
import copy
from . import parse_def
from types import SimpleNamespace

def analyze_hand_model(hand_obj):
    aka_dora_count = 0

    # === 1) 全部まとめて生牌列作る ===
    raw_tiles = hand_obj.hand_pai + [hand_obj.winning_pai]

    tiles_cleaned = []
    for tile in raw_tiles:
        if tile.endswith("'"):
            aka_dora_count += 1
            tile = tile[:-1]  # 'を外す
        # 5m → m5 に
        if len(tile) == 2 and tile[1] in "mps":
            tile = tile[1] + tile[0]
        tiles_cleaned.append(tile)

    # === 2) 副露も変換 ===
    for meld in hand_obj.huuro:
        new_tiles = []
        for t in meld["tiles"]:
            if len(t) == 2 and t[1] in "mps":
                t = t[1] + t[0]
            new_tiles.append(t)
        meld["tiles"] = new_tiles

    # === 3) 反映 ===
    hand_obj.hand_pai = tiles_cleaned[:-1]  # 和了牌以外
    hand_obj.winning_pai = tiles_cleaned[-1]

    # === 4) 解析 ===
    hand_numeric = parse_def.tile_strs_to_indices(hand_obj)
    melds = parse_def.parse_huuro_to_melds(hand_obj)
    agari_patterns = parse_def.can_form_agari_numeric(hand_obj)
    mentsu_to_dict = parse_def.mentsu_to_dict

    if not agari_patterns:
        return {
            "agari_patterns": [],
            "melds": melds,
            "melds_descriptions": [],
            "error_message": "和了形が作れません。牌が不足しているか、面子が作れません。",
            "aka_dora_count": aka_dora_count,
        }

    first_pattern = agari_patterns[0]
    melds_descriptions = [
        parse_def.describe_mentsu(mentsu_to_dict(m)) for m in first_pattern[0]
    ]

    return {
        "agari_patterns": agari_patterns,
        "melds": melds,
        "melds_descriptions": melds_descriptions,
        "error_message": "",
        "aka_dora_count": aka_dora_count,
    }
