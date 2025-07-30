from MSC.models import ScoreResult
from MSC.logic.validation.validator import validate_hand
from MSC.logic.evaluator import evaluate_hand
from MSC.logic.object import full_flow

from MSC.logic.object.han import YakuCounter
from MSC.logic.object.han import Yakumann
from MSC.models import Condition
from MSC.logic.score_calc_1.calculate_hu import calculate_fu
from MSC.logic.score_calc_1.calculate_point import calculate_score_from_yakumann
def calculate_score(hand, condition):
    # ① Handオブジェクトを解析役判定＋妥当性チェックする
    result=full_flow.run_full_flow(hand.hand_pai,hand.winning_pai,hand.huuro ,condition)

    # ③ 符数・翻数・点数計算
    evaluation_result = evaluate_hand(hand, condition)

    # ④ 結果をScoreResult形式にまとめて返す
    return ScoreResult(
        han=result['han'],
        fu=evaluation_result['fu'],
        point=evaluation_result['point'],
        yaku_list=result['yaku_list'],
        error_message=result["error_message"]
    # ② 妥当性チェック
    validation_error = validate_hand(parsed_hand, condition)
    if validation_error:
        # エラーがある場合は、ScoreResultをエラー付きで返す
        return ScoreResult(
            han=0,
            fu=0,
            point=0,
            yaku_list=[],
            error_message=validation_error
        )
    
    # ③ 役判定＋符数・翻数・点数計算
    if Yakumann == None:
        sum_score = calculate_point(han: int, fu: int, is_tsumo: bool, is_oya: bool, condition:Condition)
    else:
        sum_score = calculate_point_from_yakumann(yakumann_obj, is_tsumo: bool, is_oya: bool)
    calc_hu = calculate_fu(hand_instance, condition_instance, agari_pattern,is_chiitoitsu)
    
    # ④ 結果をScoreResult形式にまとめて返す
    return ScoreResult(
        han=evaluation_result['han'],
        fu = calc_hu['fu'],
        point = sum_score['score'],
        yaku_list=evaluation_result['yaku_list'],
        error_message=""
    )