from django.urls import path
from . import views

urlpatterns = [
    path('tic_tac_toe/',views.tic_tac_toe,name='tic_tac_toe')
]
