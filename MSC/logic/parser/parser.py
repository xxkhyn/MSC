class ParsedHand:
    def __init__(self, tiles, winning_tile, huuro, dora):
        self.tiles = tiles
        self.winning_tile = winning_tile
        self.huuro = huuro
        self.dora = dora

def parse_hand(hand_obj):
    return ParsedHand(
        tiles=hand_obj.hand_pai,
        winning_tile=hand_obj.winning_pai,
        huuro=hand_obj.huuro,
        dora=hand_obj.dora_pai
    )