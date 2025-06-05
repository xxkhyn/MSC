from django.shortcuts import render, redirect, get_object_or_404 
from .forms import ConditionForm, HandForm
from .models import Condition, Hand, ScoreResult
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

def index_view(request):
    hand_form = HandForm()
    condition_form = ConditionForm()

    return render(request, 'MSC/index.html', {
        'hand_form': hand_form,
        'condition_form': condition_form,
    })

@csrf_exempt
def condition_submit_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            condition = Condition.objects.create(
                is_riichi = data.get("is_riichi", False),
                is_ippatsu=data.get("is_ippatsu", False),
                prevalent_wind=data.get("prevalent_wind", "east"),
                seat_wind=data.get("seat_wind", "east"),
            )
            return JsonResponse({"success": True, "condition_id": condition.id})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=405)

def hand_input_view(request):
    """手牌入力用ビュー＾"""
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
    
    else :
        form = HandForm()

    return render(request, 'MSC/hand.html', {'form': form})

def score_result_view(request, result_id):
    result = get_object_or_404(ScoreResult, pk=result_id)
    return render(request, "MSC/score_result.html", {"result": result})



