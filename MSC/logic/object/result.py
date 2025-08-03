import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from MSC.models import Condition
from MSC.logic.calculator import calculate_score
from types import SimpleNamespace

def test_calculate_score_with_huuro():
    # ===== 副露ありの手牌 =====
    hand_pai = ['m2', 'm3', 'm4', 'm5', 'm6', 'm7', 's7', 's8', 's9', 'z5', 'z5']  # 手牌（11枚）
    winning_pai = 'z5'  # 和了牌は白
    huuro = [
        {
            "type": "pon",
            "tiles": ["m8", "m8", "m8"]
        }
    ]

    Hand = SimpleNamespace(
        hand_pai=hand_pai,
        winning_pai=winning_pai,
        is_huuro=False,
        is_tsumo = False,
        huuro = []
    )

    cond = Condition(
        seat_wind='east',
        prevalent_wind='east',
        is_riichi=False,
        is_double_riichi=False,
        is_ippatsu=False,
        is_rinshan=False,
        is_chankan=False,
        is_haitei=False,
        is_houtei=False,
        is_tenho=False,
        is_tsumo=True,
    )

    result = calculate_score(Hand, cond)

    print("=== 副露ありの ScoreResult ===")
    print(f"Han (翻数): {result.han}")
    print(f"Fu (符数): {result.fu}")
    print(f"Point (点数): {result.point}")
    print(f"Yaku List (役一覧): {result.yaku_list}")
    print(f"Error: {result.error_message}")

if __name__ == '__main__':
    test_calculate_score_with_huuro()
