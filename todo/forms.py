from django import forms
from .models import Todo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo
        fields = ['title', 'description', 'important']

class UserCreateForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['password2'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['username'].help_text = None