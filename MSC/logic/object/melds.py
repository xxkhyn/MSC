import sys
import os
import django
from collections import Counter
from typing import List, Tuple
import copy
from MSC.logic.parser.parser import analyze_hand_model

# melds.py の場所から見て、ルートの絶対パスを追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'msc_project.config.settings')
django.setup()

"""analyze_hand_modelを引き出せばmodelsのすべての処理を引き出せる
    手牌の解析（アガれる形かどうか・面子構成の確認・）
    手牌配列と副露が別で送られてくるので、副露の情報を反映させつつ
    副露を含めた手牌を送る。

    返し値：
    解析済み手牌・ガれなかった場合のエラーアメッセージ
"""


# 手牌オブジェクト内の手牌配列を数値化する
TILE_TO_INDEX = {
    **{f"m{i}": i-1 for i in range(1, 10)},
    **{f"p{i}": 9 + i-1 for i in range(1, 10)},
    **{f"s{i}": 18 + i-1 for i in range(1, 10)},
    **{f"z{i}": 27 + i-1 for i in range(1, 8)},
}

# 手牌配列を数値化する関数
def tile_strs_to_indices(tiles: List[str]) -> List[int]:
    indices = []
    for t in tiles:
        if t not in TILE_TO_INDEX:
            raise ValueError(f"未知の牌表記: {t}")
        indices.append(TILE_TO_INDEX[t])
    return indices

def can_form_agari_numeric(hand: List[int]) -> List[Tuple[List[List[int]], List[int]]]:
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
                results.append((copy.deepcopy(mentsu_list), [i, i]))
    return results

def _can_form_mentsu_numeric(counts: Counter, result: List[List[int]]) -> bool:
    if not counts:
        return True
    tile = min(counts)
    c = counts[tile]
    if c >= 3:
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

def parse_huuro_to_melds(huuro_data: List[dict]) -> List[dict]:
    melds = []
    for item in huuro_data:
        meld_type = item.get("type")
        tiles_str = item.get("tiles", [])
        is_open = item.get("open", True)
        tiles_num = tile_strs_to_indices(tiles_str)
        if meld_type == "chi":
            melds.append({"type": "shuntsu", "tiles": tiles_num, "open": is_open})
        elif meld_type == "pon":
            melds.append({"type": "kotsu", "tiles": tiles_num, "open": is_open})
        elif meld_type == "kan":
            melds.append({"type": "kan", "tiles": tiles_num, "open": is_open})
    return melds

from types import SimpleNamespace

# 擬似的に models.Hand のインスタンスのように振る舞うオブジェクトを作る
def create_hand_instance(hand_pai, winning_pai, huuro=None):
    if huuro is None:
        huuro = []
    return SimpleNamespace(hand_pai=hand_pai, winning_pai=winning_pai, huuro=huuro)

# 例: テスト用の牌配列
test_hand_pai = ["m1", "m2", "m3", "p4", "p5", "p6", "s7", "s8", "s9", "z1", "z1", "z2", "z2"]
test_winning_pai = "z2"
is_huuro = True
hand_instance = create_hand_instance(test_hand_pai, test_winning_pai)

# analyze_hand_model関数に渡して結果を取得
result = analyze_hand_model(hand_instance)

print(result)