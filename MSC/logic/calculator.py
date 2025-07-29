from MSC.models import ScoreResult
from MSC.logic.parser.parser import analyze_hand_model as parse_hand
from MSC.logic.validation.validator import validate_hand
from MSC.logic.evaluator import evaluate_hand


def calculate_score(hand, condition):
    # ① Handオブジェクトを解析する
    parsed_hand = parse_hand(hand)

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
    evaluation_result = evaluate_hand(parsed_hand, condition)

    # ④ 結果をScoreResult形式にまとめて返す
    return ScoreResult(
        han=evaluation_result['han'],
        fu=evaluation_result['fu'],
        point=evaluation_result['point'],
        yaku_list=evaluation_result['yaku_list'],
        error_message=""
    )