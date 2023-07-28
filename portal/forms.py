from django import forms
from django.contrib.auth.models import User

from random import randint

from .models import Colaborator, ItemToBuy


class FileInformation(forms.Form):
    file = forms.FileField()
    

class ItemToBuyForm(forms.ModelForm):
    class Meta:
        model = ItemToBuy
        fields = '__all__'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class LoginForm(forms.Form):
    # class Meta:
    #     model = User
    #     fields = ['username', 'password']
    
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        # 'value': 'januario95'    
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        # 'value': 'Jaci1995'    
    }))
    


class BinarySearchForm(forms.Form):
    number1 = forms.IntegerField()
    number2 = forms.IntegerField()
    number3 = forms.IntegerField()
    number4 = forms.IntegerField()
    number5 = forms.IntegerField()
    number6 = forms.IntegerField()
    number7 = forms.IntegerField()
    number8 = forms.IntegerField()
    number9= forms.IntegerField()
    

class CollaboratorForm(forms.ModelForm):
    # email = forms.EmailField(widget=forms.EmailInput(attrs={
    #     'placeholder': 'first.last@portal.co.mz',
    #     'value': 'first.last@portal.co.mz'
    # }))
    
    class Meta:
        model = Colaborator
        fields = ['first_name', 'last_name',
                  'department', 'division', 'job_title']
        
        
        