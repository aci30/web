from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-id')
    def popular(self):
        return self.order_by('-rating')

class Question(models.Model):
    objects = QuestionManager()
    title = models.CharField(max_length=255)
    text = models.TextField(default='q_placeholder')
    added_at = models.DateTimeField(auto_now_add=True, null=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    likes = models.ManyToManyField(User, related_name='question_likes_user', null=True)

    def build_url(self):
        return reverse('question', kwargs={'id': self.id})

    def __str__(self):
        return self.title

class Answer(models.Model):
    text = models.TextField(default='a_placeholder')
    added_at = models.DateTimeField(auto_now_add=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.text