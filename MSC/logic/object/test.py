import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


import django
django.setup()

# 以降にDjangoモデルのimportや使用を書く
from MSC.models import Condition
from MSC.logic.yaku.judge_yaku import judge_yaku

import random

from MSC.logic.yaku.judge_yaku import judge_yaku  # あなたの役判定関数
from MSC.logic.parser import parse_def       # 牌の変換などに使う想定

# 牌種類（34種）を表すインデックスリスト
ALL_TILES = list(range(34))

def generate_random_hand():
    # 14枚の手牌をランダムに生成
    # 実際は34枚を超えないように枚数制限かけるのが理想
    # ここでは簡易的に34種から14枚無作為に抽出（重複あり）
    return random.choices(ALL_TILES, k=14)

def hand_indices_to_str(hand_indices):
    # parse_def.NUMERIC_TO_TILEなど使って文字列配列に変換
    # ここは例として、仮にNUMERIC_TO_TILEが辞書であれば
    return [parse_def.NUMERIC_TO_TILE[i] for i in hand_indices]

def test_random_hands(n=1000):
    for i in range(n):
        hand_indices = generate_random_hand()
        hand_strs = hand_indices_to_str(hand_indices)
        
        # 役判定に渡すために整形 (例)
        parsed_hand = {
            "mentsu": None,  # ここは必要に応じて生成 or モック
            "pair": None,
            "tiles_count": [0]*34,
            "winning_tile_index": hand_indices[-1],  # 適当に最後の牌を上がり牌に
        }

        # 牌カウント更新
        for t in hand_indices:
            parsed_hand["tiles_count"][t] += 1

        try:
            result = judge_yaku(parsed_hand)
        except Exception as e:
            print(f"Error on hand {hand_strs}: {e}")
            raise

    print(f"All {n} random hands tested without error!")

if __name__ == "__main__":
    test_random_hands(1000)