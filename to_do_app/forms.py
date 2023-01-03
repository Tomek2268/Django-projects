from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    
    class Meta:
        model = Task
        fields = ['title','body','done']

    def __init__(self,*args,**kwargs):
        super(TaskForm, self).__init__(*args,**kwargs)
        
        for name,field in self.fields.items():
            if name == 'done':
                field.widget.attrs.update({'class':'form-check-input'})
            else:
                field.widget.attrs.update({'class':'form-control'})

