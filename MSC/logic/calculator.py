"""点数計算実行ファイル"""

# 各計算ファイルからimportする
from MSC.models import ScoreResult

def calculate_score(Hand, Condition):

    """点数計算実行関数。返し値は点数結果オブジェクト。"""

    try:

        # 手牌解析処理

        # 妥当性チェック

        # 点数計算と役判定

        # ScoreResultオブジェクトの生成

        score_result = ScoreResult.objects.create(

        )

        return score_result
    
    except Exception as e:
        return ScoreResult.objects.create(
            han=0, fu=0, point=0, yaku_list=[], error_message=str(e)
        )
    