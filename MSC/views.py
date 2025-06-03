from django.shortcuts import render, redirect, get_object_or_404 
from .forms import ConditionForm, HandForm
from .models import Condition, Hand, ScoreResult

def index_view(request):
    hand_form = HandForm()
    condition_form = ConditionForm()

    return render(request, 'MSC/index.html', {
        'hand_form': hand_form,
        'condition_form': condition_form,
    })

def condition_input_view(request):
    """条件入力用ビュー"""
    if request.method == 'POST':
        form = ConditionForm(request.POST)
        if form.is_valid():
            # 辞書展開でフィールドをそのまま渡す
            condition = Condition.objects.create(form.cleaned_data)
            return redirect('calculate_score', condition_id=condition.id)
    else:
        form = ConditionForm()

    return render(request, 'MSC/condition_form.html', {
        'form': form
    })

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



