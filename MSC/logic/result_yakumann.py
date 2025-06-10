from msc_project.MSC.logic.object import Yakumann
from msc_project.MSC.logic.国士無双 import is_kokushi
from msc_project.MSC.models import Condition

class PointCalculator:
    def __init__(self, yakumann_count: int, is_tsumo: bool, is_oya: bool):
        self.yakumann_count = yakumann_count
        self.is_tsumo = is_tsumo
        self.is_oya = is_oya

    def calculate(self):
        result = {
            "hand_type": "",#役満、三倍満など
            "score": ""#実際の合計点数
        }
        if self.yakumann_count <= 0:
            return {"hand_type":"yakumann_error",
                    "score" : "0"
                    }

        base = 16000 
        multiplier = self.yakumann_count

        #if self.is_tsumo:
        if self.is_oya:
            result["score"]  = str(base * 3 * multiplier)     
        else:
               
            result["score"] =  str(base * 2 * multiplier)
        result["hand_type"] = f"{multiplier}倍役満"
        return result
        '''else:  # ロン
            total = 48000 * multiplier if self.is_dealer else 32000 * multiplier
            return {
                "total": total,
                "note": f"{multiplier}倍役満（ロン）"
            }'''


'''class ScoreCalculator:
    def calculate_base_point(han) -> int:
            if self.total_han == 1:
                return 8000
            elif self.total_han == 2:
                return 16000
            elif self.total_han == 3:
                return 32000
            elif self.total_han == 4:
                return 64000
            elif self.total_han == 5:
                return 128000
        if han == "yakumann":#役満
        return 8000
    elif han >= 13:
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
        return min(hu * (2 ** (2 + han)), 2000)
def calculate_score(han:str,is_tumo:bool,is_oya:bool):
    base = calculate_base_point(han)
    result = {
        "base_point": base, #もととなる点数
        "hand_type":"",     #役満、三倍満、満貫など
        "score": ""         #実際の点数支払い
    }
    if han == "yakumann":
        result["hand_type"] = "役満"
    elif han >= 13:
        result["hand_type"] = "数え役満"
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

    return result'''
