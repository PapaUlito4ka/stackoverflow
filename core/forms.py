from django import forms
from core.models import User, Question, Answer


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64, 
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64, 
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User


class QuestionForm(forms.Form):
    title = forms.CharField(label='Title', max_length=64, 
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6}), label='Body')
    tags = forms.CharField(label='Tags', max_length=64, 
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Question


class AnswerForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6}))

    class Meta:
        model = Answer
