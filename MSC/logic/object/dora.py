
def next_dora_tile(tile_str: str) -> str:
    """
    表示牌からドラを返す。
    - 数牌なら 1 → 2、9 → 1
    - 字牌なら 東 → 南 → 西 → 北 → 白 → 発 → 中 → 東
    """
    suits = ["m", "p", "s"]
    honors = ["z1", "z2", "z3", "z4", "z5", "z6", "z7"]  # 東南西北白発中

    suit, num = tile_str[0], tile_str[1:]

    if suit in suits:
        next_num = str(int(num) + 1) if int(num) < 9 else "1"
        return f"{suit}{next_num}"
    elif suit == "z":
        index = honors.index(tile_str)
        next_index = (index + 1) % len(honors)
        return honors[next_index]
    else:
        raise ValueError(f"Unknown tile: {tile_str}")


def normalize_tile(tile_str: str) -> str:
    """牌文字列から赤ドラマーク（'）を外す"""
    return tile_str[:-1] if tile_str.endswith("'") else tile_str

def count_dora(hand_pai: list, winning_pai: str, dora_list: list) -> int:
    dora_tiles = [next_dora_tile(d) for d in dora_list]
    
    # 赤ドラマークを外して正規化
    normalized_hand = [normalize_tile(t) for t in hand_pai + [winning_pai]]

    return sum(normalized_hand.count(d) for d in dora_tiles)
