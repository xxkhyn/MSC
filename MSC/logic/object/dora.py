def next_dora_tile(tile_str: str) -> str:
    """
    表示牌からドラを返す。
    - 数牌なら 1 → 2、9 → 1
    - 字牌なら 東 → 南 → 西 → 北 → 白 → 発 → 中 → 東
    """
    suits = ["m", "p", "s"]
    honors = ["1z", "2z", "3z", "4z", "5z", "6z", "7z"]  # 東南西北白発中

    num, suit = tile_str[:-1], tile_str[-1]

    if suit in suits:
        next_num = str(int(num) + 1) if int(num) < 9 else "1"
        return next_num + suit
    elif suit == "z":
        index = honors.index(tile_str)
        next_index = (index + 1) % len(honors)
        return honors[next_index]
    else:
        raise ValueError(f"Unknown tile: {tile_str}")

def count_dora(hand_pai: list, winning_pai: str, dora_list: list) -> int:
    """
    手牌と和了牌に含まれるドラの数をカウントする
    """
    dora_tiles = [next_dora_tile(d) for d in dora_list]
    all_tiles = hand_pai + [winning_pai]
    return sum(all_tiles.count(d) for d in dora_tiles)
