from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('to_do_list/<int:page>/',views.to_do_list,name='to_do_list'),
    path('create_task/',views.create_task,name='create_task'),
    path('task/<str:pk>/',views.task,name='task'),
    path('delete_task/<str:pk>/',views.delete_task,name='delete_task'),
]