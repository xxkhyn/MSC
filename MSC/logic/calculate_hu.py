import math
class hu_caluculate:
    def calculate_fu(is_tsumo: bool, is_closed: bool, melds: list, pair_tile: str, wait_type: str, player_wind: str, round_wind: str) -> int:
        fu = 20 if is_tsumo else 30  # 副底符

        # 雀頭が役牌かどうか
        yaku_tiles = [player_wind, round_wind, 'z5', 'z6', 'z7']  # 自風・場風・三元牌
        if pair_tile in yaku_tiles:
            fu += 2

        # 面子の符を加算（meldsは例: [{'type': 'pon', 'tile': '5m', 'closed': True}, ...]）
        for meld in melds:
            t = meld['type']  # pon, chi, kan
            tile = meld['tile']
            closed = meld['closed']
            is_terminal_or_honor = tile[0] in ['1', '9', 'z']

            if t == 'pon':
                if is_terminal_or_honor:
                    fu += 8 if closed else 4
                else:
                    fu += 4 if closed else 2
            elif t == 'kan':
                if is_terminal_or_honor:
                    fu += 32 if closed else 16
                else:
                    fu += 16 if closed else 8

        # 待ち形の符（単騎・ペンチャン・カンチャン）
        if wait_type in ['tanki', 'kanchan', 'penchan']:
            fu += 2

        # 門前ツモの場合、2符追加
        if is_tsumo and is_closed:
            fu += 2

        # 最後に10の倍数に切り上げ
        fu = math.ceil(fu / 10) * 10
        return fu
