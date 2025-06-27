from MSC.logic.object.han import YakuCounter
from MSC.models import Condition
from MSC.logic.score_calc_1.calculate_hu import hu_calculate
import math

class ScoreCalculator:
    @staticmethod
    def calculate_base_point(han,hu) -> int:
        if han >= 13:
            return 8000  # 役満
        elif han >= 11:
            return 6000  # 三倍満
        elif han >= 8:
            return 4000  # 倍満
        elif han >= 6:
            return 3000  # 跳満
        elif han >= 5:
            return 2000  # 満貫
        elif han == 4 and hu >= 40:
            return 2000  # 満貫
        elif han == 3 and hu >= 70:
            return 2000  # 満貫
        else:
            # 基本点 = 符 × 2^(2 + 翻)
            return hu * (2 ** (2 + han))
    @staticmethod
    def round_up_100(value: int) -> int:
        return math.ceil(value / 100) * 100
    def calculate_score(han:int,hu:int,is_tumo:bool,is_oya:bool):
        base = ScoreCalculator.calculate_base_point(han, hu)
        base = ScoreCalculator.round_up_100(base)
        result = {
            "base_point": base, #もととなる点数
            "hand_type":"",     #役満、三倍満、満貫など
            "score": ""         #実際の点数支払い
        }
    
        if han >= 13:
            result["hand_type"] = "役満"
        elif han >= 11:
            result["hand_type"] = "三倍満"
        elif han >= 8:
            result["hand_type"] = "倍満"
        elif han >= 6:
            result["hand_type"] = "跳満"
        elif base == 2000:
            result["hand_type"] = "満貫"    #翻数で満貫、役満などの判定、resultに格納
    
        if is_tumo:
            if is_oya:
                result["score"] = f"{base*2}オール"#親でツモった場合
            else:
                result["score"] = f"{base},{base*2}"#子でツモった場合
        else:
            if is_oya:
                result["score"] = f"{base*6}"#親でロンした場合
            else:
                result["score"] = f"{base*4}"#子でロンした場合

        return result
