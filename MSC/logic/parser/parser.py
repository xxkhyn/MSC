import copy
from . import parse_def
from types import SimpleNamespace

def analyze_hand_model(hand_obj):
    # 赤ドラカウント用
    aka_dora_count = 0

    # 牌文字列から index へ
    raw_tiles = hand_obj.hand_pai + [hand_obj.winning_pai] + sum(hand_obj.huuro, [])

    original_hand_len = len(hand_obj.hand_pai)
    tiles_cleaned = []

    for tile in raw_tiles:
        if tile.endswith("'"):
            aka_dora_count += 1
            tiles_cleaned.append(tile[:-1])
        else:
            tiles_cleaned.append(tile)

    hand_obj.hand_pai = tiles_cleaned[:original_hand_len]
    hand_obj.winning_pai = tiles_cleaned[original_hand_len]
    # 改修: cleaned だけを使って numeric 化
    hand_obj.hand_pai = tiles_cleaned[:len(hand_obj.hand_pai)]
    hand_obj.winning_pai = tiles_cleaned[len(hand_obj.hand_pai)]
    # huuro は flat なので slice しない
    # → 必要なら同じように分割する

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
            "aka_dora_count": aka_dora_count,  # 追加
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
        "aka_dora_count": aka_dora_count,  # 追加
    }