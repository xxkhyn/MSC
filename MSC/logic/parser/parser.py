import copy
from . import parse_def
from types import SimpleNamespace
from MSC.logic.yaku.yaku import is_kokushi, is_kokushi_13machi, is_chiitoitsu
from collections import Counter
from MSC.logic.object.han import Yakumann, YakuCounter

KOKUSHI_INDICES = [
    0, 8, 9, 17, 18, 26, 27, 28, 29, 30, 31, 32, 33
]

def analyze_hand_model(hand_obj):
    aka_dora_count = 0

    # === 1) 正規化 ===
    raw_tiles = hand_obj.hand_pai + [hand_obj.winning_pai]

    tiles_cleaned = []
    for tile in raw_tiles:
        if tile.endswith("'"):
            aka_dora_count += 1
            tile = tile[:-1]
        if len(tile) == 2 and tile[1] in "mps":
            tile = tile[1] + tile[0]
        tiles_cleaned.append(tile)

    for meld in hand_obj.huuro:
        new_tiles = []
        for t in meld["tiles"]:
            if len(t) == 2 and t[1] in "mps":
                t = t[1] + t[0]
            new_tiles.append(t)
        meld["tiles"] = new_tiles

    hand_obj.hand_pai = tiles_cleaned[:-1]
    hand_obj.winning_pai = tiles_cleaned[-1]

    hand_numeric = parse_def.tile_strs_to_indices(hand_obj)
    melds = parse_def.parse_huuro_to_melds(hand_obj)
    agari_patterns = parse_def.can_form_agari_numeric(hand_obj)
    mentsu_to_dict = parse_def.mentsu_to_dict

    yakumann = Yakumann()
    yakucounter = YakuCounter()

    # 特殊役判定（和了形がない場合）
    if not agari_patterns:
        tiles_count = [0] * 34
        for t in tiles_cleaned:
            idx = parse_def.TILE_TO_NUMERIC[t]
            tiles_count[idx] += 1
        winning_idx = parse_def.TILE_TO_NUMERIC[hand_obj.winning_pai]

        print(f"tiles_count: {tiles_count}")
        print(f"winning_idx: {winning_idx}, in kokushi: {winning_idx in KOKUSHI_INDICES}")

        if is_kokushi_13machi(tiles_count, winning_idx, yakumann):
            print("国士無双十三面待ち判定OK")
            # 国士13面待ち判定がTrueなら国士無双通常判定はしない（elifで排他）
            kokushi_tiles = [parse_def.NUMERIC_TO_TILE[idx] for idx in KOKUSHI_INDICES]
            agari_patterns = []
            wait_tiles = []
            for tile_str in kokushi_tiles:
                agari_patterns.append(([[tile_str]], None))
                wait_tiles.append(tile_str)
            return {
                "kokushi_13machi": True,
                "agari_patterns": agari_patterns,
                "melds": [],
                "wait": wait_tiles,
                "melds_descriptions": [],
                "error_message": "",
                "aka_dora_count": aka_dora_count,
            }
        elif is_kokushi(tiles_cleaned, yakumann):
            print("国士無双判定OK")
            kokushi_pattern = [[[parse_def.NUMERIC_TO_TILE[idx]] for idx in KOKUSHI_INDICES], None]
            agari_patterns = [kokushi_pattern]
            wait_tile = hand_obj.winning_pai
            return {
                "kokushi": True,
                "agari_patterns": agari_patterns,
                "melds": [],
                "wait": [wait_tile],
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
            return {
                "chiitoitsu": True,
                "agari_patterns": [[pairs, None]],
                "melds": [],
                "wait": [hand_obj.winning_pai],  # 和了牌を待ち牌にセット
                "melds_descriptions": ["七対子"],
                "error_message": "",
                "aka_dora_count": aka_dora_count,
            }

    # 通常の和了形がある場合はそのまま返す
    return {
        "agari_patterns": agari_patterns,
        "melds": melds,
        "melds_descriptions": [],  # 必要に応じて設定してください
        "wait": [],  # 通常形は待ち牌は後で計算してもよいので一旦空リスト
        "error_message": "",
        "aka_dora_count": aka_dora_count,
    }
