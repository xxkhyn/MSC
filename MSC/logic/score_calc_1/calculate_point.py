"""符、翻数を引数にして実際の点数を返り値とする"""
from MSC.logic.object.han import YakuCounter
from MSC.logic.object.han import Yakumann
from MSC.models import Condition
from MSC.logic.score_calc_1.calculate_hu import calculate_fu
import math

class ScoreCalculator:
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
    def calculate_base_point(han, fu) -> int:
        if han >= 13:
            return 8000  # 数え役満
        elif han >= 11:
            return 6000  # 三倍満
        elif han >= 8:
            return 4000  # 倍満
        elif han >= 6:
            return 3000  # 跳満
        elif han >= 5:
            return 2000  # 満貫
        elif han == 4 and fu >= 40:
            return 2000
        elif han == 3 and fu >= 70:
            return 2000
        else:
            return fu * (2 ** (2 + han))

    @staticmethod
    def calculate_score(han: int, fu: int, is_tsumo: bool, is_oya: bool):
        base = ScoreCalculator.calculate_base_point(han, fu)
        base = ScoreCalculator.round_up_100(base)

        result = {
            "base_point": base,
            "hand_type": "",
            "score": ""
        }

        if han >= 13:
            result["hand_type"] = "数え役満"
        elif han >= 11:
            result["hand_type"] = "三倍満"
        elif han >= 8:
            result["hand_type"] = "倍満"
        elif han >= 6:
            result["hand_type"] = "跳満"
        elif base == 2000:
            result["hand_type"] = "満貫"
        else:
            result["hand_type"] = f"{han}翻{fu}符"

        if is_tsumo:
            result["score"] = f"{base * 2}オール" if is_oya else f"{base},{base * 2}"
        else:
            result["score"] = f"{base * 6}" if is_oya else f"{base * 4}"

        return result
