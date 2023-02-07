from django.db import models
from django.contrib.auth.models import User
import uuid
import sys
 
# setting path
sys.path.append('../games')
 
# importing
from games.models import TicTacToeGame

# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE,related_name='recipient',null=True,blank=True)
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=500,blank=True,null=True)
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    class Meta:
        ordering = ['is_read','-created']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True)

    @property
    def unread_messages(self):
        unread = Message.objects.filter(recipient=self.user,is_read=False).count()
        return unread

    @property
    def has_game(self):
        try:
            game = TicTacToeGame.objects.get(invited=self.user)
            return True
        except:
            return False