def detect_wait_type(tiles, winning_tile, pair_tiles):
    from collections import Counter
    tile_counts = Counter(tiles)

    # 単騎判定：和了牌が雀頭牌のうち1枚だけなら単騎待ち
    if winning_tile in pair_tiles and tile_counts[winning_tile] == 1:
        return 'tanki'

    num = int(winning_tile[0])
    suit = winning_tile[1]
    is_numbered = suit in ['m', 'p', 's']

    if not is_numbered:
        return 'shanpon'

    def tile_str(n): return f"{n}{suit}"

    # シャンポン待ち（刻子の片割れ）
    if tile_counts[winning_tile] == 2:
        return 'shanpon'

    # 両面待ち判定
    if (num > 1 and tile_str(num - 1) in tiles) and (num < 9 and tile_str(num + 1) in tiles):
        return 'ryanmen'

    # カンチャン、ペンチャン判定
    if (num > 1 and tile_str(num - 1) in tiles) or (num < 9 and tile_str(num + 1) in tiles):
        # ペンチャンの端判定
        if (num == 3 and tile_str(1) in tiles and tile_str(2) in tiles) or \
           (num == 7 and tile_str(8) in tiles and tile_str(9) in tiles):
            return 'penchan'
        return 'kanchan'

    return 'unknown'
