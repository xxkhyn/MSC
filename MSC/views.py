from django.shortcuts import render, redirect, get_object_or_404
from .forms import ConditionForm, HandForm
from .models import Condition, Hand, ScoreResult
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from MSC.logic import calculator # test_calculatorは未使用のためコメントアウトしてもOK
import json

def index_view(request):
    hand_form = HandForm()
    condition_form = ConditionForm()
    
    # ページ表示時に前回結果は表示しないように修正
    return render(request, 'MSC/index.html', {
        'hand_form': hand_form,
        'condition_form': condition_form,
        'result': None, # 常にNoneを渡す
    })

@csrf_exempt
def condition_submit_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # デバック用コード
            print("\n条件受信データ：\n", data)
            print('\n')

            # is_tsumoがHandからConditionに移動したことに対応
            condition = Condition.objects.create(
                is_riichi=data.get("is_riichi", False),
                is_ippatsu=data.get("is_ippatsu", False),
                is_rinshan=data.get("is_rinshan", False),
                is_chankan=data.get("is_chankan", False),
                is_haitei=data.get("is_haitei", False),
                is_tenho=data.get("is_tenho", False),
                prevalent_wind=data.get("prevalent_wind", "east"),
                seat_wind=data.get("seat_wind", "east"),
                player_type=data.get("player_type", "child"), # デフォルトを子に
                kyotaku=int(data.get('kyotaku', 0)),
                honba=int(data.get('honba', 0)),
                # is_tsumo は Hand にあるためここでは不要
            )
            return JsonResponse({"success": True, "condition_id": condition.id})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=405)

def hand_input_view(request):
    """手牌入力用ビュー（現在はAPI経由のため直接は使われない可能性が高い）"""
    if request.method == 'POST':
        form = HandForm(request.POST)
        if form.is_valid():
            hand = Hand.objects.create(
                hand_pai=form.cleaned_data['hand_pai'],
                winning_pai=form.cleaned_data['winning_pai'],
                is_huuro=form.cleaned_data['is_huuro'],
                huuro=form.cleaned_data['huuro'],
                dora_pai=form.cleaned_data['dora_pai']
            )
            return redirect('condition_input', hand_id=hand.id)
    else:
        form = HandForm()

    return render(request, 'MSC/hand.html', {'form': form})

@csrf_exempt
def hand_input_api(request):
    """JSONを受け取ってHandを作成するAPI"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # デバック用コード
            print("\n手牌受信データ：\n", data)
            print('\n')

            # ★★★ ここからが修正箇所 ★★★
            # 'hand_pai' というキーが存在しない場合のみエラーにする
            if 'hand_pai' not in data:
                return JsonResponse({'error': 'hand_pai key is missing'}, status=400)

            # Hand作成（JavaScriptの配列をそのまま受け取る）
            hand = Hand.objects.create(
                hand_pai=data.get('hand_pai', []),
                winning_pai=data.get('winning_pai'), # nullを受け取れるように
                is_tsumo=data.get('is_tsumo', True), # is_tsumoはこちらで受け取る
                is_huuro=data.get('is_huuro', False),
                huuro=data.get('huuro', []),
                dora_pai=data.get('dora_pai', [])
            )
            return JsonResponse({'hand_id': hand.id}, status=201)
            # ★★★ 修正ここまで ★★★

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

@csrf_exempt
def calculate_score_api(request):
    if request.method == 'POST':
        try:
            hand = Hand.objects.last()
            condition = Condition.objects.last()

            if hand is None:
                raise ValueError("Hand データが存在しません")
            if condition is None:
                raise ValueError("Condition データが存在しません")

            print("\n手牌オブジェクト:", hand)
            print("\n条件オブジェクト:", condition)

            try:
                result_obj = calculator.calculate_score(hand, condition)
                print("\n▶ calculate_score 成功:", result_obj)
            except Exception as e:
                import traceback
                traceback.print_exc()
                return JsonResponse({
                    "success": False,
                    "error": f"\ncalculate_score で例外: {e}"
                }, status=500)

            # ScoreResult をDBに保存
            score_result = ScoreResult.objects.create(
                han=result_obj.han,
                fu=result_obj.fu,
                point=result_obj.point,
                yaku_list=result_obj.yaku_list,
                error_message=result_obj.error_message
            )

            # デバック用コード
            print("計算結果:", score_result)
            print('\n')

            # result_id を返す
            return JsonResponse({
                "success": True,
                "result_id": score_result.id
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=405)

def score_result_api_view(request, result_id):
    result = get_object_or_404(ScoreResult, pk=result_id)
    data = {
        "han": result.han,
        "fu": result.fu,
        "point": result.point,
        "yaku_list": result.yaku_list,
        "error_message": result.error_message or "",
    }
    return JsonResponse(data)

def how_to_use_view(request):
    return render(request, 'MSC/tukaikata.html')

def scocal_map_view(request):
    return render(request, 'MSC/hayami.html')
