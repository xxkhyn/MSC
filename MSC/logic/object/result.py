import os
import django

# Django セットアップ
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # ← プロジェクト名に合わせて
django.setup()

from MSC.models import Condition, ScoreResult
from MSC.logic.calculator import calculate_score
from types import SimpleNamespace


def test_calculate_score():
    # ===== テスト用のダミー手牌 =====
    hand_pai = ['m1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'z1', 'z1', 'z1', 'z1']
    winning_pai = 'z1'
    huuro = []  # 副露なし

    Hand = SimpleNamespace(
        hand_pai=hand_pai,
        winning_pai=winning_pai,
        huuro=huuro
    )

    cond = Condition(
        seat_wind='east',
        prevalent_wind='east',
        is_riichi=True,
        is_double_riichi=False,
        is_ippatsu=False,
        is_rinshan=False,
        is_chankan=False,
        is_haitei=False,
        is_houtei=False,
        is_tenho=False,
        is_tsumo=True
    )

    # ===== スコア計算実行 =====
    result = calculate_score(Hand, cond)

    # ===== 結果を表示 =====
    print("=== ScoreResult ===")
    print(f"Han (翻数): {result.han}")
    print(f"Yaku List (役一覧): {result.yaku_list}")
    print(f"Error: {result.error_message}")


# ここ重要！テスト関数を呼ぶ
if __name__ == '__main__':
    test_calculate_score()
