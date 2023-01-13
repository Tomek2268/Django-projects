from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Message

class RegisterForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    def __init__(self,*args,**kwargs):
        super(RegisterForm, self).__init__(*args,**kwargs)
        
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})
            if name == 'username':
                field.widget.attrs.update({'placeholder':'Username'})
            if name == 'email':
                field.widget.attrs.update({'placeholder':'Email'})
            if name == 'password1':
                field.widget.attrs.update({'placeholder':'Password'})
            if name == 'password2':
                field.widget.attrs.update({'placeholder':'Confirm password'})

class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']

    def __init__(self,*args,**kwargs):
        super(EditUserForm, self).__init__(*args,**kwargs)
        
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})

class MessageForm(forms.ModelForm):
    
    class Meta:
        model = Message
        fields = ['recipient','title','body']

    def __init__(self,*args,**kwargs):
        super(MessageForm, self).__init__(*args,**kwargs)
        
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})
            if name == 'recipient':
                #field.widget.attrs.update({'required':'True'})
                pass

