from django.urls import path

from .views import index_view

app_name = 'MSC'
urlpatterns = [
  path('', index_view, name="index")
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('hand_input/', views.hand_input_view, name='hand_input'),
    path('score_result/<int:result_id>/', views.score_result_view, name='score_result'),
    path('score_result_api/<int:result_id>/', views.score_result_api_view, name='score_result_api'),  # 追加
]
