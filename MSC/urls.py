from django.urls import path

from .views import views

app_name = 'MSC'
urlpatterns = [
    path('', views.index_view, name='index'),
    path('hand_input/', views.hand_input_view, name='hand_input'),
    path('api/hand-input/', views.hand_input_api, name='hand_input_api'),
    path('api/condition/submit/', views.condition_submit_api, name='condition_submit_api'),
    path('api/score/calculate/', views.calculate_score_api, name='calculate_score_api'),
]
