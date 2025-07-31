import sys
import os
import django
from collections import Counter
from typing import List, Tuple
import copy

# ルートパスを追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'msc_project.config.settings')
django.setup()

from MSC import models  # Hand モデルを想定

# 数値 <-> 牌文字 の変換テーブル
NUMERIC_TO_TILE = {
    **{i: f"m{i+1}" for i in range(0, 9)},
    **{i+9: f"p{i+1}" for i in range(0, 9)},
    **{i+18: f"s{i+1}" for i in range(0, 9)},
    **{i+27: f"z{i+1}" for i in range(0, 7)},
    34: "m5'",  # 赤ドラ 5萬
    35: "p5'",  # 赤ドラ 5筒（もし使うなら）
    36: "s5'",  # 赤ドラ 5索（もし使うなら）
}
TILE_TO_NUMERIC = {v: k for k, v in NUMERIC_TO_TILE.items()}


def tile_strs_to_indices(hand_obj):
    hand_pai = hand_obj.hand_pai
    indices = []
    for t in hand_pai:
        if t not in TILE_TO_NUMERIC:
            raise ValueError(f"未知の牌表記: {t}")
        indices.append(TILE_TO_NUMERIC[t])
    return indices


def all_tiles_to_indices(hand_obj):
    """
    Handオブジェクトの hand_pai + winning_pai をまとめて数値化する
    """
    tiles = hand_obj.hand_pai + [hand_obj.winning_pai]
    indices = []
    for t in tiles:
        if t not in TILE_TO_NUMERIC:
            raise ValueError(f"未知の牌表記: {t}")
        indices.append(TILE_TO_NUMERIC[t])
    return indices


def can_form_agari_numeric(hand_obj):
    """
    手牌と和了牌から和了形を探す
    """
    indices = all_tiles_to_indices(hand_obj)
    results = []
    counts = Counter(indices)
    for i in range(34):
        if counts[i] >= 2:
            temp = counts.copy()
            temp[i] -= 2
            if temp[i] == 0:
                del temp[i]
            mentsu_list = []
            if _can_form_mentsu_numeric(temp, mentsu_list):
                results.append([copy.deepcopy(mentsu_list), [i, i]])
    return results


def _can_form_mentsu_numeric(counts: Counter, result: List[List[int]]) -> bool:
    """
    再帰的に順子・刻子を構成できるか判定する
    """
    if not counts:
        return True
    tile = min(counts)
    if counts[tile] >= 3:
        result.append([tile] * 3)
        counts[tile] -= 3
        if counts[tile] == 0:
            del counts[tile]
        if _can_form_mentsu_numeric(counts, result):
            return True
        result.pop()
        counts[tile] += 3
    if tile < 27 and tile % 9 <= 6:
        t2 = tile + 1
        t3 = tile + 2
        if counts.get(t2, 0) and counts.get(t3, 0):
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


def parse_huuro_to_melds(hand_obj):
    """
    Handオブジェクトの huuro を数値に変換
    """
    melds = []
    for item in hand_obj.huuro:
        meld_type = item.get("type")
        tiles_str = item.get("tiles", [])
        is_open = item.get("open", True)
        tiles_num = [TILE_TO_NUMERIC[t] for t in tiles_str]
        melds.append({
            "type": meld_type,
            "tiles": tiles_num,
            "open": is_open
        })
    return melds



def describe_mentsu(mentsu: dict) -> str:
    """
    面子 dict を説明用の文字列にする
    """
   
    
    tiles = mentsu["tiles"]
    type_ = mentsu["type"]
    open_ = mentsu.get("open", False)

    tile_strs = [NUMERIC_TO_TILE[i] for i in tiles]
    main_tile = tile_strs[0]

    if type_ == "kotsu":
        type_name = "刻子"
    elif type_ == "kan":
        type_name = "槓子"
    elif type_ == "shuntsu":
        type_name = "順子"
    else:
        type_name = "不明"

    open_str = ""
    if type_ in {"kotsu", "kan"}:
        open_str = "(鳴き)" if open_ else "(暗刻)"
    elif type_ == "shuntsu" and open_:
        open_str = "(鳴き)"

    return f"{main_tile}{type_name}{open_str}"


def mentsu_to_dict(mentsu_tiles):
        # 刻子・順子を判別
        if len(mentsu_tiles) == 3:
            if mentsu_tiles[0] == mentsu_tiles[1] == mentsu_tiles[2]:
                type_ = "kotsu"
            elif mentsu_tiles[0] +1 == mentsu_tiles[1] and mentsu_tiles[1] +1 == mentsu_tiles[2]:
                type_ = "shuntsu"
            else:
                type_ = "不明"
        elif len(mentsu_tiles) == 4 and len(set(mentsu_tiles)) == 1:
            type_ = "kan"
        else:
            type_ = "不明"
        return {"type": type_, "tiles": mentsu_tiles, "open": False}