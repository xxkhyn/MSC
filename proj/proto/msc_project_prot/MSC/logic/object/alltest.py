from MSC.logic.object.han import Yakumann
from MSC.logic.国士無双.kokushi import is_kokushi, is_kokushi_13machi, str_to_index
from MSC.logic.object.tiles import HandProvider, MahjongParser, DataReceiver
from MSC.logic.score_calc_2.result_yakumann import PointCalculator
from MSC.models import ScoreResult
from MSC.logic.past_calculator import calculate_score
import sys
sys.path.append('~/ma-zyan')

# テスト用の入力データ例
test_data = {
    "hand_pai": "m1,m9,p1,p9,s1,s9,1,2,3,4,5,6,7",
    "winning_pai": "1",
    "is_tsumo": True,
    "is_oya": False
}

result_obj = calculate_score(test_data)

print("テスト結果:")
print(f"翻数: {result_obj.han}")
print(f"符数: {result_obj.fu}")
print(f"点数: {result_obj.point}")
print(f"役リスト: {result_obj.yaku_list}")
print(f"エラー: {result_obj.error_message}")
