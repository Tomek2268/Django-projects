from django.db import models
from django.contrib.auth.models import User
import uuid
import sys
 
# setting path
sys.path.append('../games')
 
# importing
from games.models import TicTacToeGame

# Create your models here.

class Chat(models.Model):
    members = models.ManyToManyField(User,blank=True)
    chat_name = models.CharField(max_length=30,null=True,blank=True)

    @property
    def latest_message(self):
        message = Message.objects.filter(chat=self.id).latest('created')
        return message

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE,related_name='recipient',null=True,blank=True)
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=500,blank=True,null=True)
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        ordering = ['is_read','-created']

    def length(self):
        return len(self.title)

    @property
    def created_time(self):
        return self.created.strftime("%H:%M")

    @property
    def created_date(self):
        return self.created.strftime("%d/%m/%y")

    @property
    def created_datetime(self):
        return self.created.strftime("%d/%m/%y %H:%M")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True)

    @property
    def unread_messages(self):
        unread = Message.objects.filter(recipient=self.user,is_read=False).count()
        return unread


