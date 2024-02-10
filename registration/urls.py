from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('home/', views.home, name='home'),
    path('', views.home, name='home'), # Add this line 
    path('logout/', views.user_logout, name='logout'),
    
    path('makesuperuser/<str:username>/', views.MakeSuperuserView.as_view(), name='make_superuser'),
    
]