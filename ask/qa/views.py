from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
from django.urls import reverse
from qa.models import Question, Answer

# Create your views here.
from django.http import HttpResponse 
def test(request, *args, **kwargs):
    return HttpResponse('OK')

@require_GET
def main(request):
    questions = Question.objects.new()
    limit = 10
    page_id = request.GET.get('page', 1)
    paginator = Paginator(questions, limit)
    paginator.baseurl = reverse('main')
    page = paginator.page(page_id)
    return render(request, 'main.html', {
            'questions': page.object_list,
            'paginator': paginator,
            'page' : page,
        })

@require_GET
def popular(request):
    questions = Question.objects.popular()
    limit = 10
    page_id = request.GET.get('page', 1)
    paginator = Paginator(questions, limit)
    paginator.baseurl = reverse('popular')
    page = paginator.page(page_id)
    return render(request, 'main.html', {
            'questions': page.object_list,
            'paginator': paginator,
            'page' : page,
        })

@require_GET
def question(request, id):
    question = get_object_or_404(Question, id=id)
    answers = Answer.objects.filter(question=id)
    return render(request, 'question.html', {
            'question': question,
            'answers': answers,
        })