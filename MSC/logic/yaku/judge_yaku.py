import sys
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "msc_project.config.settings")
django.setup()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from MSC.logic.yaku.yaku import (
    is_tanyao, is_pinfu, is_iipeikou, is_chiitoitsu,
    is_ryanpeikou, is_toitoi,
    # 他の役もあれば追加
)
from logic.object.han import YakuCounter


def judge_yaku(parsed_hand, huuro=None):
    yaku_counter = YakuCounter()
    
    # huuro（副露）あり・なしで判定を変えたい場合
    huuro = huuro or []
    
    # 役判定群を順番に呼ぶ（例）
    is_tanyao(parsed_hand, yaku_counter, huuro)
    is_pinfu(parsed_hand, yaku_counter, huuro)
    is_iipeikou(parsed_hand, yaku_counter, huuro)
    is_chiitoitsu(parsed_hand, yaku_counter)
    is_ryanpeikou(parsed_hand, yaku_counter, huuro)
    is_toitoi(parsed_hand, yaku_counter)
    # ... 必要な役判定を全部
    
    # 最後に重複排除
    yaku_counter.resolve_conflicts()
    
    # 役判定結果を辞書やリストで返す
    return yaku_counter.yaku

parsed_hand = {
    "mentsu": [
        {"type": "shuntsu", "tiles": ["m1", "m2", "m3"], "open": False},
        {"type": "kotsu", "tiles": ["z1", "z1", "z1"], "open": False},
        {"type": "kotsu", "tiles": ["p7", "p7", "p7"], "open": False},
        {"type": "shuntsu", "tiles": ["s4", "s5", "s6"], "open": False}
    ],
    "pair": {"type": "simple", "tiles": ["m9", "m9"]},
    "wait": "ryanmen"
}

result = judge_yaku(parsed_hand, huuro=[])
print(result)
