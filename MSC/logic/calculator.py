from MSC.logic.object.han import Yakumann
from MSC.logic.国士無双.kokushi import is_kokushi, is_kokushi_13machi, str_to_index
from MSC.logic.object.tiles import HandProvider, MahjongParser, DataReceiver
from MSC.logic.result_yakumann import PointCalculator
from MSC.models import ScoreResult


def calculate_score(cleaned_data: dict):
    try:
        provider = HandProvider(cleaned_data)
        receiver = DataReceiver(provider)
        tiles = receiver.parsed_data

        winning_tile = cleaned_data["winning_pai"]
        win_idx = str_to_index(winning_tile)
        tiles[win_idx] += 1

        is_tsumo = cleaned_data.get("is_tsumo", False)
        is_oya = cleaned_data.get("is_oya", False)

        yakuman_counter = Yakumann()
        if is_kokushi(tiles):
            if is_kokushi_13machi(tiles, win_idx):
                yakuman_counter.add_yaku("国士無双十三面待ち", 2)
            else:
                yakuman_counter.add_yaku("国士無双", 1)

        if yakuman_counter.get_total() > 0:
            pc = PointCalculator(
                yakumann_count=yakuman_counter.get_total(),
                is_tsumo=is_tsumo,
                is_oya=is_oya
            )
            result = pc.calculate()
            # ScoreResultオブジェクト作成して返す例
            return ScoreResult.objects.create(
                han=yakuman_counter.get_total() * 13,
                fu=0,
                point=result["score"],
                yaku_list=list(yakuman_counter.get_yakus().keys()),
                error_message=""
            )

        # 通常役処理
        '''han = cleaned_data.get("han", 3)
        fu = cleaned_data.get("fu", 40)

        score_data = ScoreCalculator.calculate_score(han, fu, is_tsumo, is_oya)

        return ScoreResult.objects.create(
            han=han,
            fu=fu,
            point=score_data["score"],
            yaku_list=score_data.get("yakus", []),
            error_message=""
        )'''

    except Exception as e:
        return ScoreResult.objects.create(
            han=0, fu=0, point=0, yaku_list=[], error_message=str(e)
        )
