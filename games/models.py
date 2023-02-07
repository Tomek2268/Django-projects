from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TicTacToeGame(models.Model):
    room = models.CharField(max_length=50,null=True,blank=True,unique=True)
    host = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    invited = models.OneToOneField(User,on_delete=models.CASCADE,related_name='invited',null=True,blank=True)
    game_on = models.BooleanField(default=True)



    mark = models.TextField(max_length=1,default='O',null=True,blank=True)
    library_of_board = models.JSONField(max_length=9,default=dict)
    legal_moves = models.JSONField(max_length=9,default=list)

    rejected = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)

    win = models.BooleanField(default=False)
    outcome = models.CharField(max_length=10,default='false') 