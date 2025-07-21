def validate_hand(parsed_hand, condition):
    # 例：牌が14枚未満 → エラー
    if len(parsed_hand.tiles) + 1 != 14:
        return "手牌が14枚ではありません（副露考慮は必要）"
    # 例：和了牌が空 → エラー
    if not parsed_hand.winning_tile:
        return "和了牌が未設定です"

    # 他にもルールチェックを入れる
    return None  # エラーがなければ None