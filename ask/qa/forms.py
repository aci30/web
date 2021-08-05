from django import forms
from qa.models import Question, Answer
from django.contrib.auth.models import User

from hashlib import sha256

class AskForm(forms.Form):
    title = forms.CharField(max_length=50, label='Title')
    text = forms.CharField(label='Question', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(AskForm, self).__init__(*args, **kwargs)

    def clean(self):
        pass

    def save(self):
        return Question.objects.create(**self.cleaned_data)


class AnswerForm(forms.Form):
    text = forms.CharField(label='Answer')
    question = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)

    def clean(self):
        pass

    def save(self):
        question = Question.objects.get(id=self.cleaned_data['question'])
        answer = Answer(text=self.cleaned_data['text'], question=question)
        answer.save()
        return answer

class SignupForm(forms.Form):
    username = forms.CharField(label='Username', required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    email = forms.EmailField(label='Email', required=False)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        if not 3 < len(username) <= 20:
            raise forms.ValidationError('Invalid username length')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('User already exists')
        return username

    def clean(self):
        pass

    def save(self):
        return User.objects.create_user(**self.cleaned_data)