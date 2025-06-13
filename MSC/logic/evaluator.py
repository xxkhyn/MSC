KOKUSHI_REQUIRED_TILES = {
    '1m', '9m',
    '1p', '9p',
    '1s', '9s',
    'z1', 'z2', 'z3', 'z4', 'z5', 'z6', 'z7'
}

def evaluate_hand(parsed_hand, condition):
    # 国士無双の判定
    tiles = parsed_hand.tiles + [parsed_hand.winning_tile]  # 和了牌も含めた14枚

    tile_counts = {}
    for tile in tiles:
        tile_counts[tile] = tile_counts.get(tile, 0) + 1

    # 必要牌が1枚以上あるか
    if not KOKUSHI_REQUIRED_TILES.issubset(tile_counts.keys()):
        # 必要牌が足りない → 国士無双でない
        return dummy_result()

    # 14枚ちょうどで、13種＋1種2枚になっているか？
    count_13_unique = sum(1 for tile in KOKUSHI_REQUIRED_TILES if tile_counts.get(tile, 0) >= 1)
    count_pair = any(count >= 2 for tile, count in tile_counts.items() if tile in KOKUSHI_REQUIRED_TILES)

    if count_13_unique == 13 and count_pair:
        # 国士無双成立
        return {
            "han": 13,  # 役満として13翻扱い
            "fu": 0,    # 役満なので符は関係なし
            "point": 48000 if condition.is_tsumo else 48000,  # 仮に48000点（親か子に応じて変更可能）
            "yaku_list": ["国士無双"]
        }
    else:
        # 国士無双不成立 → ダミー返却
        return dummy_result()

def dummy_result():
    return {
        "han": 0,
        "fu": 20,  # 仮符
        "point": 1000,  # 仮の安い点
        "yaku_list": []
    }