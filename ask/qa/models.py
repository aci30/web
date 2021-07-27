from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
	title = models.CharField(max_length=255)
	text = models.TextField()
	added_at = models.DateTimeField()
	rating = models.IntegerField()
	author = models.CharField(max_length=255)
	likes = models.ManyToManyField(User)

class QuestionManager():
	def new():
		return Question.objects.order_by(added_at).desc()
	def popular():
		return Question.objects.order_by(rating)


class Answer(models.Model):
	text = models.TextField()
	added_at = models.DateTimeField()
	question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
	author = models.CharField(max_length=255)