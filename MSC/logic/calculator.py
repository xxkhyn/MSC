from MSC.models import ScoreResult
from MSC.logic.validation.validator import validate_hand
from MSC.logic.evaluator import evaluate_hand
from MSC.logic.object import full_flow

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
    )