from MSC.models import ScoreResult
from MSC.logic.validation.validator import validate_hand
from MSC.logic.evaluator import evaluate_hand
from MSC.logic.object import full_flow
from MSC.logic.yaku.yaku import is_chiitoitsu
from MSC.logic.object.han import YakuCounter
from MSC.models import Condition
from MSC.logic.score_calc_1.calculate_hu import calculate_fu
from MSC.logic.score_calc_1.calculate_point import ScoreCalculator
from MSC.logic.object.han import Yakumann


def calculate_score(hand, condition):

    result=full_flow.run_full_flow(hand,condition)
    yakumann = Yakumann()
    yakumann_obj = yakumann.get_count()

    print(yakumann.get_count)
    # ① Handオブジェクトを解析役判定＋役判定＋妥当性チェックする
    # ② 符数・翻数・点数計算
    han = result['han']

    agari_patterns = result.get('agari_patterns')
    agari_pattern = agari_patterns[0]
    YAKUMAN_LIST = {"国士無双", "四暗刻", "四暗刻単騎", "九蓮宝燈", "純正九蓮宝燈", "大三元", "四槓子", "小四喜", "大四喜"}
    yakumann_obj = Yakumann()
    for yaku in result.get("yaku_list", []):
        if yaku in YAKUMAN_LIST:
            yakumann_obj.add_yaku(yaku)

    yakumann_count = yakumann_obj.get_count()
    print("役満数:", yakumann_count)
    #メンツ構成
    print(agari_pattern[0])
    #雀頭
    print(agari_pattern[1])

    fu = calculate_fu(hand, condition, agari_pattern, is_chiitoitsu) 
    #符表示
    print(fu)
    #役リスト表示
    print(result['yaku_list'])
    if condition.player_type == 'parent':
        is_oya = True
    else:
        is_oya = False
    if yakumann_count == 0:
        sum_score = ScoreCalculator.calc_point(han, fu, condition.is_tsumo, is_oya, condition)
    else:
        sum_score = ScoreCalculator.calc_point_from_yakumann(yakumann_count, condition.is_tsumo, is_oya)
    print(sum_score)
    # ④ 結果をScoreResult形式にまとめて返す
    print(han,fu,)

    return ScoreResult(
        han=han,
        fu = fu,
        point = sum_score['score'],
        yaku_list=result['yaku_list'],
        error_message=result["error_message"]
    )
   
   
