import os
import django

# Django セットアップ
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # プロジェクトに合わせて
django.setup()

from MSC.models import Condition
from MSC.logic.calculator import calculate_score
from types import SimpleNamespace

def test_calculate_score():
    # ===== テスト用のダミー手牌 =====
    # 例: 萬子1〜4の順子x3 + 東ポン + 東雀頭
    hand_pai = ['m1', 'm9', 'p1', 'p9', 's1', 's9', 'z1', 'z2', 'z3', 'z4', 'z5', 'z6', 'z7']
    winning_pai = 'm1'
    huuro = []  # 副露なし

    # Handオブジェクト風
    Hand = SimpleNamespace(
        hand_pai=hand_pai,
        winning_pai=winning_pai,
        is_huuro=False,
        is_tsumo = True,
        huuro = []
    )

    # ===== Condition =====
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

    # ===== スコア計算実行 =====
    result = calculate_score(Hand, cond)

    # ===== 結果を表示 =====
    print("=== ScoreResult ===")
    print(f"Han (翻数): {result.han}")
    print(f"Fu (符数): {result.fu}")
    print(f"Point (点数): {result.point}")
    print(f"Yaku List (役一覧): {result.yaku_list}")
    print(f"Error: {result.error_message}")
    print(f"agari_patterns:{result}")

if __name__ == '__main__':
    test_calculate_score()
