from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TicTacToeGame(models.Model):
    room = models.CharField(max_length=50,null=True,blank=True,unique=True)
    host = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    invited = models.OneToOneField(User,on_delete=models.CASCADE,related_name='invited',null=True,blank=True)

    game_continue = models.IntegerField(default=0)
    mark = models.TextField(max_length=1,default='O',null=True,blank=True)
    library_of_board = models.JSONField(max_length=9,default=dict)
    legal_moves = models.JSONField(max_length=9,default=list)