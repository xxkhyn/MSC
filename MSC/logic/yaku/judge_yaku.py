from MSC.logic.object.han import YakuCounter, Yakumann, resolve_conflicts

def judge_yaku(parsed_hand, huuro=None):
    """
    parsed_hand: {
        "mentsu": [...],
        "pair": {...},
        "wait": ...,
        "tiles_count": [...],  # optional
        "winning_tile_index": int,  # optional
    }
    huuro: 副露リスト

    役満と通常役を別々に判定し、排他処理の後、役名と翻数の辞書を返す。
    """

    if huuro is None:
        huuro = []

    yaku_counter = YakuCounter()  # 通常役カウンター
    yakumann = Yakumann()         # 役満カウンター

    # 役満判定関数群インポート
    from MSC.logic.yaku.yaku import (
        is_kokushi, is_kokushi_13machi, is_chinroutou, is_tsuuiisou,
        is_chuuren, is_ryuisou, is_daisuusii, is_sangenpai,
        is_suukantsu, is_suuankou, is_suuankou_tanki,
    )

    tiles_counts = parsed_hand.get("tiles_count", None)
    winning_tile_index = parsed_hand.get("winning_tile_index", None)

    # 役満判定
    if tiles_counts:
        is_kokushi(tiles_counts, yakumann)
        if winning_tile_index is not None:
            is_kokushi_13machi(tiles_counts, winning_tile_index, yakumann)
        is_chinroutou(tiles_counts, yakumann)
        is_tsuuiisou(tiles_counts, yakumann)

    is_chuuren(parsed_hand, yakumann)
    is_ryuisou(parsed_hand, yakumann)
    is_daisuusii(parsed_hand, yakumann)
    is_sangenpai(parsed_hand, yakumann)
    is_suukantsu(parsed_hand, yakumann)
    is_suuankou(parsed_hand, yakumann)
    is_suuankou_tanki(parsed_hand, yakumann)

    # 通常役判定関数群インポート
    from MSC.logic.yaku.yaku import (
        is_ryanpeikou,
        is_chiitoitsu, is_ikkitsuukan, is_sanshoku_doujun, is_sankantsu,
        is_sanankou, is_toitoi, is_honroutou, is_sanshoku_doukou,
        is_tanyao, is_pinfu, is_iipeikou,
    )

    # 高翻役（通常役）
    is_ryanpeikou(parsed_hand, yaku_counter, huuro)

    # 中翻役（通常役）
    is_chiitoitsu(tiles_counts, yaku_counter)
    is_ikkitsuukan(parsed_hand, yaku_counter, huuro)
    is_sanshoku_doujun(parsed_hand, yaku_counter, huuro)
    is_sankantsu(parsed_hand, yaku_counter, huuro)
    is_sanankou(parsed_hand, yaku_counter)
    is_toitoi(parsed_hand, yaku_counter)
    is_honroutou(tiles_counts, yaku_counter)
    is_sanshoku_doukou(parsed_hand, yaku_counter, huuro)

    # 低翻役（通常役）
    is_tanyao(parsed_hand, yaku_counter, huuro)
    is_pinfu(parsed_hand, yaku_counter, huuro)
    is_iipeikou(parsed_hand, yaku_counter, huuro)

    # 排他処理（役満と通常役の排他含む）
    resolve_conflicts(yaku_counter, yakumann)

    # 役満があれば役満のみ返す、なければ通常役を返す
    if yakumann.get_count() > 0:
        return {name: 13 for name in yakumann.get_yakus()}  # 役満は13翻固定など適宜調整
    else:
        return yaku_counter.get_yakus()
