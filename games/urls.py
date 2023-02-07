from django.urls import path
from . import views

urlpatterns = [
    path('tic_tac_toe/',views.tic_tac_toe,name='tic_tac_toe'),
    path('ttt_lobby/',views.ttt_lobby,name='ttt_lobby'),
    path('tic_tac_toe_online/<str:room>/',views.tic_tac_toe_online,name='tic_tac_toe_online'),
]
