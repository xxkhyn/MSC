from MSC.models import ScoreResult
from MSC.logic.validation.validator import validate_hand
from MSC.logic.evaluator import evaluate_hand
from MSC.logic.object import full_flow
from MSC.logic.yaku.yaku import is_chiitoitsu
from MSC.logic.yaku.yaku import is_kokushi
from MSC.logic.yaku.yaku import is_kokushi_13machi
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
    YAKUMAN_LIST = {"国士無双","国士無双十三面待ち","清老頭", "四暗刻", "四暗刻単騎", "九蓮宝燈", "純正九蓮宝燈", "大三元", "四槓子", "小四喜", "大四喜","清老頭"}
    yakumann_obj = Yakumann()
    for yaku in result.get("yaku_list", []):
        if yaku in YAKUMAN_LIST:
            yakumann_obj.add_yaku(yaku)

    yakumann_count = yakumann_obj.get_count()

    #役満数
    print()
    print("役満数",yakumann_count)

    #メンツ構成
    print()
    print(agari_pattern[0])

    #雀頭
    print()
    print(agari_pattern[1])
    
    #役リスト表示
    print()
    print(result['yaku_list'])
    
    yaku_list = result.get("yaku_list", [])
    if "国士無双" in yaku_list or "国士無双十三面待ち" in yaku_list:
        fu = 0  # 国士無双は符計算不要（飜数・点数は役満固定）
        print()
        print("符計算スキップ：国士無双 or 国士無双十三面待ち")
    else:
        fu = calculate_fu(hand, condition, agari_pattern, is_chiitoitsu, is_kokushi, is_kokushi_13machi)
        print()
        print("符計算結果", fu)

    #符表示
    print()
    print("符計算結果",fu)

    

    if condition.player_type == 'parent':
        is_oya = True
    else:
        is_oya = False
    if yakumann_count == 0:
        sum_score = ScoreCalculator.calc_point(han, fu, condition.is_tsumo, is_oya, condition)
    else:
        sum_score = ScoreCalculator.calc_point_from_yakumann(yakumann_count, condition.is_tsumo, is_oya)
    print()
    print(sum_score)

    # ④ 結果をScoreResult形式にまとめて返す

    print(han, fu, sum_score['score'], result['yaku_list'], result["error_message"])
    print(type(result['yaku_list']))

    result_yaku_list= list(result['yaku_list'].items())

    print(result_yaku_list)
    print(type(result_yaku_list))

    return ScoreResult(
        han=han,
        fu = fu,
        point = sum_score['score'],
        yaku_list=result_yaku_list,
        error_message=result["error_message"]
    )
   
   
