from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
from django.urls import reverse
from qa.models import Question, Answer
from qa.forms import AskForm, AnswerForm, SignupForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from hashlib import sha256
import random, string

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

def question(request, id):
    question = get_object_or_404(Question, id=id)
    answers = Answer.objects.filter(question=id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        form._user = request.user
        if form.is_valid():
            answer = Answer.objects.create(
                text = form.cleaned_data['text'],
                question = Question.objects.get(id=form.cleaned_data['question']),
                author = form._user
            )
            url = question.build_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(initial={'question': question.id})
    return render(request, 'question.html', {
            'question': question,
            'answers': answers,
            'form': form
        })

@login_required(redirect_field_name='continue')
def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        form._user = request.user
        if form.is_valid():
            question = Question.objects.create(
                title = form.cleaned_data['title'],
                text = form.cleaned_data['text'],
                author = form._user
            )
            url = question.build_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'ask.html', {
            'form': form,
        })

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            form.add_error(None, 'Invalid username / password')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {
            'form': form,
        })

def login_view(request):
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        url = request.GET.get('continue', '/')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(url)
        else:
            error = 'Invalid username / password'
    return render(request, 'login.html', {'error': error })

def logout_view(request):
    logout(request)
    url = request.GET.get('continue', '/')
    return HttpResponseRedirect(url)

def delete(request):
    type = request.GET.get('type', '')
    id = request.GET.get('id', '')
    response = HttpResponseNotFound(r'i dont understand you')
    if type == 'question' and id:
        response = delete_question(type, id, request.user)
    if type == 'answer' and id:
        response = delete_answer(type, id, request.user)
    return response
    
def delete_question(type, id, user):
    try:
        question = Question.objects.get(id=id)
    except Question.DoesNotExist:
        return HttpResponseNotFound(r'cant delete question {id} cuz it DoesNotExist')
    if user != question.author:
        return HttpResponseRedirect(question.build_url())
    question.delete()
    return HttpResponseRedirect('/')

def delete_answer(type, id, user):
    try:
        answer = Answer.objects.get(id=id)
    except Answer.DoesNotExist:
        return HttpResponseNotFound(r'cant delete answer {id} cuz it DoesNotExist')
    if user != answer.author:
        return HttpResponseRedirect(answer.question.build_url())
    answer.delete()
    return HttpResponseRedirect(answer.question.build_url())

@login_required(redirect_field_name='continue')
def user_view(request, nickname):
    user = get_object_or_404(User, username=nickname)
    if request.method == 'POST':
        pass
    else:
        pass
    return render(request, 'user.html', {
            'user': user,
        })