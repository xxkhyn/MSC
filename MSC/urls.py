from django.urls import path

from . import views

app_name = 'MSC'

urlpatterns = [
  path('', views.index_view, name="index"),
  path('api/condition/submit/', views.condition_submit_api, name='condition_submit_api'),
  path('api/score/calculate/', views.calculate_score_api, name='calculate_score_api'),
]