from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
from django.urls import reverse
from qa.models import Question, Answer, Session
from qa.forms import AskForm, AnswerForm, SignupForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

from hashlib import sha256
import random, string, datetime

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

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            session_id, session_expires = do_login(
                    form.cleaned_data['username'], form.cleaned_data['password']
                )
            if session_id:
                response = HttpResponseRedirect('/')
                response.set_cookie('sessionid', session_id,
                        path='/', httponly=True,
                        expires = session_expires
                    )
                return response
            else:
                form.add_error(None, 'Invalid username / password')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {
            'form': form,
        })

def login(request):
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        url = request.POST.get('continue', '/')
        session_id, session_expires = do_login(username, password)
        if session_id:
            response = HttpResponseRedirect(url)
            response.set_cookie('sessionid', session_id,
                    path='/', httponly=True,
                    expires = session_expires
                )
            return response
        else:
            error = 'Invalid username / password'
    return render(request, 'login.html', {'error': error })

def do_login(username, password):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None, None
    if user.password != password:
        return None, None
    session = Session()
    session.key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
    session.user = user
    session.expires = datetime.datetime.now() + datetime.timedelta(days=1)
    session.save()
    return session.key, session.expires

def logout(request):
    session_id = request.COOKIES.get('sessionid')
    if session_id is not None:
        Session.objects.filter(key=session_id).delete()
    url = request.GET.get('continue', '/')
    response = HttpResponseRedirect(url)
    response.set_cookie('sessionid', session_id,
                    path='/', httponly=True,
                    expires = datetime.datetime.now() - datetime.timedelta(days=999)
                )
    return response