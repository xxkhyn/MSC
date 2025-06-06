import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from msc_project.MSC.logic.result_yakumann import PointCalculator

class TestPointCalculator(unittest.TestCase):

    def test_single_yakuman_oya(self):
        calc = PointCalculator(yakumann_count=1, is_tsumo=True, is_oya=True)
        result = calc.calculate()
        self.assertEqual(result["score"], "48000")
        self.assertEqual(result["hand_type"], "1倍役満")

    def test_single_yakuman_ko(self):
        calc = PointCalculator(yakumann_count=1, is_tsumo=True, is_oya=False)
        result = calc.calculate()
        self.assertEqual(result["score"], "32000")
        self.assertEqual(result["hand_type"], "1倍役満")

    def test_double_yakuman_oya(self):
        calc = PointCalculator(yakumann_count=2, is_tsumo=True, is_oya=True)
        result = calc.calculate()
        self.assertEqual(result["score"], "96000")
        self.assertEqual(result["hand_type"], "2倍役満")

    def test_invalid_no_yakuman(self):
        calc = PointCalculator(yakumann_count=0, is_tsumo=True, is_oya=False)
        result = calc.calculate()
        self.assertIn("error", result)

if __name__ == '__main__':
    unittest.main()
