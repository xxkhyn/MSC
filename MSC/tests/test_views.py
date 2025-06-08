import json
from django.test import TestCase, Client
from MSC.models import Hand, Condition, ScoreResult

"""条件テスト"""
class ConditionApiTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_condition_submit_success(self):
        payload = {
            "is_riichi": True,
            "is_ippatsu": False,
            "prevalent_wind": "east",
            "seat_wind": "south"
        }

        response = self.client.post(
            '/api/condition/submit/',
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data["success"])
        self.assertIn("condition_id", json_data)
        self.assertEqual(Condition.objects.count(), 1)


"""手牌テスト"""
class HandApiTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_hand_input_success(self):
        payload = {
            "hand_pai": ["1m", "2m", "3m", "4p", "5p", "6p", "7s", "8s", "9s", "1p", "2p", "3p", "4m"],
            "winning_pai": "5p",
            "is_huuro": True,
            "huuro": [],
            "dora_pai": ["6p", "6p"]
        }

        response = self.client.post(
            '/api/hand-input/',
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        json_data = response.json()
        self.assertIn("hand_id", json_data)
        self.assertEqual(Hand.objects.count(), 1)

    def test_hand_input_missing_hand_pai(self):
        # hand_pai がない → エラーになる
        payload = {
            "winning_pai": "5p"
        }

        response = self.client.post(
            '/api/hand-input/',
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        json_data = response.json()
        self.assertIn("error", json_data)


"""得点計算テスト"""
class CalculateScoreApiTest(TestCase):
    def setUp(self):
        self.client = Client()
        # 事前にHandとConditionを1件作成
        self.hand = Hand.objects.create(
            hand_pai=["1m", "2m", "3m", "4p", "5p", "6p", "7s", "8s", "9s", "1p", "2p", "3p", "4m"],
            winning_pai="5p",
            is_huuro=False,
            huuro=[],
            dora_pai=["6p"]
        )
        self.condition = Condition.objects.create(
            is_riichi=True,
            is_ippatsu=False,
            prevalent_wind="east",
            seat_wind="south"
        )

    def test_calculate_score_success(self):
        response = self.client.post(
            '/api/score/calculate/',
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data["success"])
        self.assertIn("result", json_data)
        result = json_data["result"]
        self.assertIn("han", result)
        self.assertIn("fu", result)
        self.assertIn("point", result)
        self.assertIn("yaku_list", result)

"""点数表示テスト"""
class ScoreResultApiTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.result = ScoreResult.objects.create(
            han=3,
            fu=40,
            point=7700,
            yaku_list=["立直", "一発", "門前清自摸和"],
            error_message=""
        )

    def test_score_result_view_success(self):
        response = self.client.get(f'/api/score/result/{self.result.id}/')

        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data["han"], 3)
        self.assertEqual(json_data["fu"], 40)
        self.assertEqual(json_data["point"], 7700)
        self.assertEqual(json_data["yaku_list"], ["立直", "一発", "門前清自摸和"])

