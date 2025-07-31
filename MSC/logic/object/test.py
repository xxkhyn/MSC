import os
import django

# Django セットアップ（必要なら）
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from MSC.logic.object.full_flow import run_full_flow
from MSC.models import Condition,Hand
from types import SimpleNamespace


def test_run_full_flow():
    hand_pai = ['m1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9','m1','m2','m3','m1']
    winning_pai = 'm4'
    huuro = []
    dora_pai = ['m5']

    Hand = SimpleNamespace(
        hand_pai=hand_pai,
        winning_pai=winning_pai,
        huuro=huuro,
        dora_pai=dora_pai
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
        is_tsumo=True,
    )

    result = run_full_flow(hand_pai, winning_pai, huuro, condition=cond)

    print("=== Full Flow Result ===")
    print("Han:", result["han"])
    print("Yaku List:", result["yaku_list"])
    print("Agari Patterns:", result["agari_patterns"])
    
    agari = result["agari_patterns"]

    print(agari[0][0])

    print(agari[0][1])

    print("Meld Descriptions:", result["melds_descriptions"])
    print("Error:", result["error_message"])


   
if __name__ == '__main__':
    test_run_full_flow()
