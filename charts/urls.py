from django.urls import path
from . import views

urlpatterns = [
    path('candlestick_chart/', views.candlestick_chart, name='candlestick_chart'),
    path('api/chart-data/', views.get_chart_data, name='chart-data'),
    path('api/timezone_offset/', views.get_timezone_offset, name='get_timezone_offset'),
    path('api/get_xtimes_preds/<str:coin_type>/<str:interval>', views.get_xtimes_preds, name='get_xtimes_preds'),
    path('api/get_chart_data/<str:symbol>/<str:interval>/<str:timestamp>/<str:location>/', views.get_chart_data, name='get_chart_data'),
]