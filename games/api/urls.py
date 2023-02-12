from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    #TTT api
    path('',views.get_routes),
    path('user_joined/',views.user_joined),
    path('user_left/',views.user_left),
    path('player_move/',views.player_move),
    path('game_continue/',views.game_continue),
    #Chat api
    path('user_joined_chat/',views.user_joined_chat),
    path('send_message/',views.send_message),
    path('user_left_chat/',views.user_left_chat),
]
