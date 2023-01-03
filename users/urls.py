from django.urls import path

from . import views

urlpatterns = [
    path('login/',views.login_view,name='login'),
    path('register/',views.register_view,name='register'),
    path('logout/',views.logout_view,name='logout'),
    path('account/',views.account,name='account'),
    path('edit_account/',views.edit_account,name='edit_account'),
    path('change_password/',views.change_password,name='change_password'),
    #Messages
    path('inbox/<int:page>/',views.inbox,name='inbox'),
    path('single_message/<str:pk>/',views.single_message,name='single_message'),
    path('message_form/<str:pk>/<has_recipient>/',views.message_form,name='message_form'),
    path('delete_message/<str:pk>/',views.delete_message,name='delete_message'),
]
