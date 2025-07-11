from MSC.models import Condition
from MSC.logic.object.melds import TILE_TO_INDEX

def calculate_fu(hand_instance, condition_instance, agari_pattern) -> int:
    mentsu_list, head = agari_pattern
    fu = 20  # 基本符（ツモ時）

    # 和了の形式による初期符設定
    if not hand_instance.is_tsumo:
        fu = 30  # ロンは30符が基本（面前ロンでピンフ以外）

    # 雀頭の符（自風 or 場風 or 三元牌）
    def is_yakuhai(index):
        return index in [
            TILE_TO_INDEX[f"z{1 + ['east','south','west','north'].index(condition_instance.seat_wind)}"],
            TILE_TO_INDEX[f"z{1 + ['east','south','west','north'].index(condition_instance.prevalent_wind)}"],
            TILE_TO_INDEX["z5"], TILE_TO_INDEX["z6"], TILE_TO_INDEX["z7"]
        ]
    if is_yakuhai(head[0]):
        fu += 2

    # 面子ごとの符計算
    for m in mentsu_list:
        tile = m[0]
        is_terminal_or_honor = tile >= 27 or tile % 9 in [0, 8]
        is_open = False
        if isinstance(m, dict):
            is_open = m.get("open", False)
            m = m["tiles"]
            tile = m[0]
            is_terminal_or_honor = tile >= 27 or tile % 9 in [0, 8]

        if len(m) == 3 and m[0] == m[1] == m[2]:  # 刻子
            if is_terminal_or_honor:
                fu += 4 if is_open else 8
            else:
                fu += 2 if is_open else 4
        elif len(m) == 4:  # カン子
            if is_terminal_or_honor:
                fu += 16 if is_open else 32
            else:
                fu += 8 if is_open else 16

    # ツモ符（面前のみ）
    if hand_instance.is_tsumo and not hand_instance.is_huuro:
        fu += 2

    # 単騎待ちなら +2符
    winning_tile = TILE_TO_INDEX[hand_instance.winning_pai]
    if head[0] == winning_tile:
        fu += 2

    # ピンフ（すべてシュンツ、面前、ツモ、待ちが両面）なら符は20符のまま
    if _is_pinfu(mentsu_list, head, winning_tile, hand_instance.is_huuro, hand_instance.is_tsumo):
        return 20

    # 符は10の倍数に切り上げ
    return ((fu + 9) // 10) * 10

def _is_pinfu(mentsu_list, head, winning_tile, is_huuro, is_tsumo):
    if is_huuro:
        return False
    from collections import Counter
    if TILE_TO_INDEX["z1"] <= head[0] <= TILE_TO_INDEX["z7"]:
        return False  # ヤクハイの頭
    for m in mentsu_list:
        if m[0] == m[1] == m[2]:  # 刻子があればピンフでない
            return False
    # 仮実装: 両面待ち判定は未実装
    return is_tsumo
