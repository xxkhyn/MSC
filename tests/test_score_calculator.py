# tests/test_score_calculator.py の最初の方に追加
import django
import os
import sys

# 必要に応じてパスを追加（例：msc_project を見えるようにする）
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# settings モジュールの指定（あれば環境変数は無視されてもOK）
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'msc_project.config.settings')

# Django の初期化（これがないと AppRegistryNotReady が出る）
django.setup()

import unittest
from MSC.logic.score_calc_1.calculate_point import ScoreCalculator


# ダミー役満オブジェクト
class DummyYakuman:
    def __init__(self, count):
        self._count = count

    def count(self):
        return self._count

class TestScoreCalculator(unittest.TestCase):

    def test_役満_親ツモ(self):
        yakuman = DummyYakuman(1)
        result = ScoreCalculator.calculate_score_from_yakumann(yakuman, is_tsumo=True, is_oya=True)
        self.assertEqual(result["base_point"], 8000)
        self.assertEqual(result["score"], "16000オール")

    def test_役満_子ロン(self):
        yakuman = DummyYakuman(1)
        result = ScoreCalculator.calculate_score_from_yakumann(yakuman, is_tsumo=False, is_oya=False)
        self.assertEqual(result["score"], "32000")

    def test_満貫_子ロン(self):
        result = ScoreCalculator.calculate_score(han=3, fu=70, is_tsumo=False, is_oya=False)
        self.assertEqual(result["base_point"], 2000)
        self.assertEqual(result["score"], "8000")

    def test_満貫_親ツモ(self):
        result = ScoreCalculator.calculate_score(han=5, fu=30, is_tsumo=True, is_oya=True)
        self.assertEqual(result["base_point"], 2000)
        self.assertEqual(result["score"], "4000オール")

    def test_4翻40符_子ツモ(self):
        result = ScoreCalculator.calculate_score(han=4, fu=40, is_tsumo=True, is_oya=False)
        self.assertEqual(result["hand_type"], "満貫")
        self.assertEqual(result["score"], "2000,4000")

    def test_3翻60符_子ロン(self):
        result = ScoreCalculator.calculate_score(han=3, fu=60, is_tsumo=False, is_oya=False)
        self.assertEqual(result["hand_type"], "3翻60符")
        self.assertEqual(result["base_point"], 1920)
        self.assertEqual(result["score"], "7700")

    def test_数え役満(self):
        result = ScoreCalculator.calculate_score(han=13, fu=30, is_tsumo=False, is_oya=True)
        self.assertEqual(result["hand_type"], "数え役満")
        self.assertEqual(result["base_point"], 8000)
        self.assertEqual(result["score"], "48000")

    def test_2翻40符_親ロン(self):
        result = ScoreCalculator.calculate_score(han=2, fu=40, is_tsumo=False, is_oya=True)
        self.assertEqual(result["hand_type"], "2翻40符")
        self.assertEqual(result["base_point"], 640)
        self.assertEqual(result["score"], "3900")
if __name__ == "__main__":
    unittest.main()
