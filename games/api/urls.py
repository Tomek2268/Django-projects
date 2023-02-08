from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),

    path('',views.get_routes),
    path('tic_tac_toe/<str:pk>/',views.get_tic_tac_toe),
    path('tic_tac_toe/<str:pk>/update/',views.update_tic_tac_toe),
    path('user_joined/',views.user_joined),
    path('user_left/',views.user_left),
    path('player_move/',views.player_move),
]
