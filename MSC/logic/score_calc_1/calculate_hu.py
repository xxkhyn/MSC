from MSC.logic.object.melds import TILE_TO_INDEX

def calculate_fu(hand_instance, condition_instance, agari_pattern) -> int:
    mentsu_list, head = agari_pattern
    winning_tile = TILE_TO_INDEX[hand_instance.winning_pai]
    fu = 20 if hand_instance.is_tsumo else 30  # 面前ロンは30符、面前ツモは20符

    # 雀頭が役牌（場風、自風、三元牌）なら +2符
    def is_yakuhai(index):
        winds = ['east', 'south', 'west', 'north']
        yakuhai_indices = [
            TILE_TO_INDEX[f"z{1 + winds.index(condition_instance.seat_wind)}"],
            TILE_TO_INDEX[f"z{1 + winds.index(condition_instance.prevalent_wind)}"],
            TILE_TO_INDEX["z5"], TILE_TO_INDEX["z6"], TILE_TO_INDEX["z7"]
        ]
        return index in yakuhai_indices
    if is_yakuhai(head[0]):
        fu += 2

    # 面子ごとの符計算
    for m in mentsu_list:
        is_open = False
        if isinstance(m, dict):
            is_open = m.get("open", False)
            m = m["tiles"]
        tile = m[0]
        is_terminal_or_honor = tile >= 27 or tile % 9 in [0, 8]

        if len(m) == 3 and m[0] == m[1] == m[2]:  # 刻子
            fu += 4 if is_open and is_terminal_or_honor else \
                  2 if is_open else \
                  8 if is_terminal_or_honor else 4
        elif len(m) == 4:  # 槓子（カン）
            fu += 16 if is_open and is_terminal_or_honor else \
                  8 if is_open else \
                  32 if is_terminal_or_honor else 16

    # 面前ツモなら +2符（ただしピンフなら除く）
    if hand_instance.is_tsumo and not hand_instance.is_huuro:
        fu += 2

    # 待ち形による +2符
    machi_type = get_machi_type(mentsu_list, head, winning_tile)
    if machi_type in ["tanki", "kanchan", "penchan"]:
        fu += 2

    # ピンフ判定（ピンフなら常に20符固定）
    if _is_pinfu(mentsu_list, head, winning_tile, hand_instance.is_huuro, hand_instance.is_tsumo):
        return 20

    return ((fu + 9) // 10) * 10  # 符は10の倍数に切り上げ


def get_machi_type(mentsu_list, head, winning_tile):
    if head[0] == winning_tile:
        return "tanki"

    for m in mentsu_list:
        if winning_tile in m:
            if len(m) == 3 and m[0] != m[1]:  # 順子
                sorted_m = sorted(m)
                if sorted_m[1] == winning_tile:
                    return "kanchan"
                elif sorted_m[0] == winning_tile and sorted_m[0] % 9 == 6:
                    return "penchan"
                elif sorted_m[2] == winning_tile and sorted_m[2] % 9 == 2:
                    return "penchan"
                else:
                    return "ryanmen"
    return None

def _is_pinfu(mentsu_list, head, winning_tile, is_huuro, is_tsumo):
    if is_huuro:
        return False
    if head[0] >= TILE_TO_INDEX["z1"]:  # 字牌の頭は役牌の可能性あり
        return False
    for m in mentsu_list:
        if len(m) == 3 and m[0] == m[1] == m[2]:
            return False  # 刻子があるとピンフではない
    machi_type = get_machi_type(mentsu_list, head, winning_tile)
    return is_tsumo and machi_type == "ryanmen"
