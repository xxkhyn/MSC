import sys
import os
import django

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from MSC.logic.object import tiles, melds
from MSC.logic.yaku.judge_yaku  import judge_yaku
from types import SimpleNamespace

def run_full_flow(hand_pai, winning_pai, huuro=None):
    huuro = huuro or []

    hand_numeric = melds.tile_strs_to_indices(hand_pai + [winning_pai])
    melds_data = melds.parse_huuro_to_melds(huuro)
    agari_patterns = melds.can_form_agari_numeric(hand_numeric)


 # tiles_countを作成する例
    from collections import Counter
    count = Counter(hand_pai + [winning_pai])
    tiles_count = [0] * 34

    for tile_str, c in count.items():
    # 1枚だけリストにして関数に渡し、結果の0番目を使う
        idx = melds.tile_strs_to_indices([tile_str])[0]
    tiles_count[idx] = c

    parsed_hand = {
        "hand_numeric": hand_numeric,
        "agari_patterns": agari_patterns,
        "melds": melds_data,
        "huuro": huuro,
        "tiles_count": tiles_count,  # 追加
        "winning_tile_index": melds.tile_strs_to_indices(hand_pai + [winning_pai])
    }

    yaku_result = judge_yaku(parsed_hand)

    return {
        "agari_patterns": agari_patterns,
        "melds": melds_data,
        "yaku": yaku_result,
    }

if __name__ == "__main__":
    test_hand_pai = ["m1", "m2", "m3", "p4", "p5", "p6", "s7", "s8", "s9", "z1", "z1", "z2", "z2"]
    test_winning_pai = "z2"
    test_huuro = []

    result = run_full_flow(test_hand_pai, test_winning_pai, test_huuro)
    print(result)
