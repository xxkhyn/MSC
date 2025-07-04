def detect_wait_type(tiles, winning_tile):
    """
    手牌とアガリ牌から待ち形を判定する
    優先順位：単騎 > カンチャン > ペンチャン > 両面 > シャンポン > 不明
    """
    from collections import Counter

    # 和了牌の数を数える（雀頭との一致判定などに使う）
    tile_counts = Counter(tiles)

    # 単騎待ち（アガリ牌が対子になるだけ）
    if tile_counts[winning_tile] == 1:
        return 'tanki'

    # 和了牌の種類分解
    num = int(winning_tile[0])
    suit = winning_tile[1]
    is_numbered = suit in ['m', 'p', 's']
    if not is_numbered:
        return 'shanpon'  # 字牌は順子にできない＝刻子 or 対子の待ち＝シャンポン

    # 順子構成のチェック
    def tile_str(n): return f"{n}{suit}"

    # カンチャン（2つ飛び）
    if tile_str(num - 1) in tiles and tile_str(num + 1) in tiles:
        return 'kanchan'

    # ペンチャン（1-2-3 や 7-8-9 の端）
    if (num == 3 and tile_str(1) in tiles and tile_str(2) in tiles) or \
       (num == 7 and tile_str(8) in tiles and tile_str(9) in tiles):
        return 'penchan'

    # 両面待ち
    if tile_str(num - 1) in tiles or tile_str(num + 1) in tiles:
        return 'ryanmen'

    # シャンポン（刻子にアガリ牌を重ねるだけ）
    if tile_counts[winning_tile] == 2:
        return 'shanpon'

    return 'unknown'
