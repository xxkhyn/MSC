"""符、翻数を引数にして実際の点数を返り値とする"""
from MSC.logic.object.han import YakuCounter
from MSC.logic.object.han import Yakumann
from MSC.models import Condition
#from MSC.logic.score_calc_1.calculate_point import calculate_fu
import math

class ScoreCalculator:#han.pyのYakumannから役満の数を受け取り、そこから条件分岐により点数計算
    @staticmethod
    def calculate_base_point_from_yakumann(yakumann_count: int) -> int:
        return 8000 * yakumann_count

    @staticmethod
    def round_up_100(value: int) -> int:
        return math.ceil(value / 100) * 100

    @staticmethod
    def calculate_score_from_yakumann(yakumann_obj, is_tsumo: bool, is_oya: bool):
        yakumann_count = yakumann_obj.count()
        base = ScoreCalculator.calculate_base_point_from_yakumann(yakumann_count)
        base = ScoreCalculator.round_up_100(base)
        result = {
            "base_point": base,
            "hand_type": "",
            "score": ""
        }
        result["hand_type"] = f"{yakumann_count}倍役満"
        if is_tsumo:
            result["score"] = f"{base * 2}オール" if is_oya else f"{base},{base * 2}"
        else:
            result["score"] = f"{base * 6}" if is_oya else f"{base * 4}"

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
    def calculate_score(han: int, fu: int, is_tsumo: bool, is_oya: bool, condition:Condition):
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
        kyotaku = condition.kyotaku  # ロン時のみ和了者に加算

# 点数詳細と出力用文字列を作成
        if is_tsumo:
            if is_oya:
                score_val = ScoreCalculator.round_up_100(base * 2 + 100 * honba)
                score_val += 1000 * kyotaku  # 供託加算
                score_detail = {
                    "oya_all": score_val
                }
                score_text = f"{score_val}オール"
            else:
                ko_score = ScoreCalculator.round_up_100(base + 100 * honba)
                oya_score = ScoreCalculator.round_up_100(base * 2 + 100 * honba)
                total_score = ko_score * 2 + oya_score + 1000 * kyotaku
                score_detail = {
                    "ko": ko_score,
                    "oya": oya_score,
                    "kyotaku_bonus": 1000 * kyotaku
                }
                score_text = f"{ko_score},{oya_score}"
        else:
            ron_score = ScoreCalculator.round_up_100((base * 6 if is_oya else base * 4) + 300 * honba + 1000 * kyotaku)
            score_detail = {
                "ron_score": ron_score,
                "honba_bonus": 300 * honba,
                "kyotaku_bonus": 1000 * kyotaku
            }
            score_text = str(ron_score)



        return {
            "base_point": base,#点数計算に使用した数字、表示させる際はいらないけどテスト用に残した
            "hand_type": hand_type,#満貫、跳満など
            "score": score_text,#合計点数　例.8000
            "score_detail": score_detail #子の支払い点数、親の支払い点数　例.2000,4000
        }
