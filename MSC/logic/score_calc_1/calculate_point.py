"""符、翻数を引数にして実際の点数を返り値とする"""
from MSC.logic.object.han import YakuCounter
from MSC.logic.object.han import Yakumann
from MSC.models import Condition
from MSC.logic.score_calc_1.calculate_hu import calculate_fu
import math

class ScoreCalculator:#han.pyのYakumannから役満の数を受け取り、そこから条件分岐により点数計算
    @staticmethod
    def calculate_base_point_from_yakumann(yakumann_count: int) -> int:
        return 8000 * yakumann_count

    @staticmethod
    def round_up_100(value: int) -> int:
        return math.ceil(value / 100) * 100

    @staticmethod
    def calc_point_from_yakumann(yakumann_count, is_tsumo: bool, is_oya: bool):
        base = ScoreCalculator.calculate_base_point_from_yakumann(yakumann_count)
        base = ScoreCalculator.round_up_100(base)
        result = {
            "base_point": base,
            "hand_type": "",
            "score": ""
        }
        result["hand_type"] = f"{yakumann_count}倍役満"
       
        result["score"] = base * 6 if is_oya else base * 4
        

        return result
    @staticmethod
    def calculate_base_point(han: int, fu: int) -> int:#YakuCounterから翻数を受け取り点数計算
     
        if han >= 13:
            return 8000  # 数え役満
        elif han >= 11:
            return 6000  # 三倍満
        elif han >= 8:
            return 4000  # 倍満
        elif han >= 6:
            return 3000  # 跳満
        elif han >= 5 or (han == 4 and fu >= 40) or (han == 3 and fu >= 70):
            return 2000  # 満貫
        else:
            return fu * (2 ** (2 + han))  # 満貫以下

    @staticmethod
    def calc_point(han: int, fu: int, is_tsumo: bool, is_oya: bool, condition:Condition):
        base = ScoreCalculator.calculate_base_point(han, fu)
     
        # 満貫判定
        is_mangan = False
        if han >= 13:
            hand_type = "数え役満"
            base = 8000
            is_mangan = True
        elif han >= 11:
            hand_type = "三倍満"
            base = 6000
            is_mangan = True
        elif han >= 8:
            hand_type = "倍満"
            base = 4000
            is_mangan = True
        elif han >= 6:
            hand_type = "跳満"
            base = 3000
            is_mangan = True
        elif han >= 5 or (han == 4 and fu >= 40) or (han == 3 and fu >= 70):
            hand_type = "満貫"
            base = 2000
            is_mangan = True
        else:
            hand_type = f"{han}翻{fu}符"
            # base は切り上げしない


        # 積棒と供託を取得
        honba = condition.honba  # 1本場ごとに +300点
        kyotaku = condition.kyotaku  

# 点数詳細と出力用文字列を作成
        #if is_tsumo:
        if is_oya:
            score_val = ScoreCalculator.round_up_100(base * 6)
            score_val += 1000 * kyotaku + 300 * honba

        else:
            ko_score = ScoreCalculator.round_up_100(base)
            oya_score = ScoreCalculator.round_up_100(base * 2)
            score_val = ko_score * 2 + oya_score + 1000 * kyotaku + 300 * honba
        '''else:
            score_val = ScoreCalculator.round_up_100(
            (base * 6 if is_oya else base * 4) + 300 * honba + 1000 * kyotaku
        )'''



        return {
            "base_point": base,#点数計算に使用し基本点、表示させる際はいらないけどテスト用に残した
            "hand_type": hand_type,#満貫、跳満など
            "score": score_val#合計点数　例.8000
        }