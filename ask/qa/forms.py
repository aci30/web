from django import forms
from qa.models import Question, Answer

class AskForm(forms.Form):
    title = forms.CharField(max_length=50, label='Title')
    text = forms.CharField(label='Question')

    def __init__(self, *args, **kwargs):
        super(AskForm, self).__init__(*args, **kwargs)

    def clean(self):
        pass

    def save(self):
        return Question.objects.create(**self.cleaned_data)


class AnswerForm(forms.Form):
    text = forms.CharField(label='Answer')
    question = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)

    def clean(self):
        pass

    def save(self):
        question = Question.objects.get(id=self.cleaned_data['question'])
        answer = Answer(text=self.cleaned_data['text'], question=question)
        answer.save()
        return answer