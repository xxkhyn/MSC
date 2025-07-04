from collections import Counter
from typing import List, Tuple



def can_form_agari_numeric(hand: List[int]) -> List[Tuple[List[List[int]], List[int]]]:
    """h
    与えられた14枚からアガリ形を列挙的に探索（数値版）
    戻り値: (面子リスト, 雀頭)
    """
    results = []
    counts = Counter(hand)

    for i in range(34):
        if counts[i] >= 2:
            temp = counts.copy()
            temp[i] -= 2
            if temp[i] == 0:
                del temp[i]

            mentsu_list = []
            if _can_form_mentsu_numeric(temp, mentsu_list):
                results.append((mentsu_list, [i, i]))

    return results


def _can_form_mentsu_numeric(counts: Counter, result: List[List[int]]) -> bool:
    if not counts:
        return True

    tile = min(counts)
    c = counts[tile]

    # 刻子チェック
    if c >= 3:
        result.append([tile] * 3)
        counts[tile] -= 3
        if counts[tile] == 0:
            del counts[tile]
        if _can_form_mentsu_numeric(counts, result):
            return True
        result.pop()
        counts[tile] += 3

    # 順子チェック（数牌のみ）
    if tile < 27 and tile % 9 <= 6:
        t2 = tile + 1
        t3 = tile + 2
        if counts.get(t2, 0) > 0 and counts.get(t3, 0) > 0:
            for t in [tile, t2, t3]:
                counts[t] -= 1
                if counts[t] == 0:
                    del counts[t]
            result.append([tile, t2, t3])
            if _can_form_mentsu_numeric(counts, result):
                return True
            result.pop()
            for t in [tile, t2, t3]:
                counts[t] = counts.get(t, 0) + 1

    return False

def detect_wait_type_from_agari_numeric(mentsu: List[List[int]], pair: List[int], winning_tile: int) -> str:
    if pair.count(winning_tile) == 1:
        return "tanki"

    for m in mentsu:
        if winning_tile not in m:
            continue
        if len(m) != 3:
            continue

        m_sorted = sorted(m)
        if m_sorted[0] == m_sorted[1] == m_sorted[2]:
            continue  # 刻子

        # 順子であることが確定している前提
        if winning_tile == m_sorted[1]:
            if m_sorted[0] + 1 == m_sorted[1] and m_sorted[1] + 1 == m_sorted[2]:
                return "kanchan"
        if winning_tile == m_sorted[0]:
            if m_sorted == [1, 2, 3] and winning_tile == 1:
                return "penchan"
        if winning_tile == m_sorted[2]:
            if m_sorted == [7, 8, 9] and winning_tile == 9:
                return "penchan"
        if m_sorted[0] + 1 == m_sorted[1] and m_sorted[1] + 1 == m_sorted[2]:
            return "ryanmen"

    return "unknown"

def parse_huuro_to_melds(huuro_data: List[dict]) -> List[dict]:
    """
    Handモデルのhuuro JSONから内部meld形式へ変換。
    """
    melds = []

    for item in huuro_data:
        meld_type = item.get("type")
        tiles = item.get("tiles", [])
        is_open = item.get("open", True)

        if meld_type == "chi":
            melds.append({
                "type": "shuntsu",
                "tiles": tiles,
                "open": is_open,
            })
        elif meld_type == "pon":
            melds.append({
                "type": "kotsu",
                "tiles": tiles,
                "open": is_open,
            })
        elif meld_type == "kan":
            melds.append({
                "type": "kan",
                "tiles": tiles,
                "open": is_open,
            })

    return melds
