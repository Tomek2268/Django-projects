from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Task(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=500,blank=True,null=True)
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,
                            primary_key=True,editable=False)

    class Meta:
        ordering = ['-created']

