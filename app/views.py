from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from app.forms import *
from app.models import *


def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    question = paginate(Question.objects.newest(), request)
    return render(request, 'index.html', {'questions': question})


def hot(request):
    question = paginate(Question.objects.most_popular(), request)
    return render(request, 'index.html', {'questions': question})


@login_required(login_url='/login/')
def ask(request):
    if request.method == 'GET':
        form = AskForm()
    else:
        form = AskForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            for tags in request.POST['tags'].split():
                tag = Tag.objects.get_or_create(name=tags)[0]
                question.tags.add(tag)
                question.save()
            return redirect(f"/question/{question.id}")
    return render(request, 'ask.html', {'form': form, 'errors': form.errors})


def login(request):
    redirect_to = request.GET.get('next', '/')
    error_message = None
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(redirect_to)
            else:
                error_message = "Sorry, wrong login or password"
    return render(request, 'login.html', {'form': form, 'redirect_to': redirect_to, 'error_message': error_message})


def question(request, pk):
    question = Question.objects.by_id(pk).first()
    answers = question.answers.hot()
    if request.method == 'GET':
        form = AnswerForm(auto_id=False)
    else:
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = Answer.objects.create(author=request.user,
                                           text=request.POST['text'],
                                           what_question=question)
            return redirect(f"/question/{question.id}")
    return render(request, "question.html", {"question": question, "answers": answers, 'form': form})


def registration(request):
    errors = []
    if request.method == 'GET':
        form = SignUpForm()
    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        if request.POST['password'] != request.POST['password_confirm']:
            errors.append('Bad password confirm')
        elif form.is_valid():
            req_data = request.POST
            user = User.objects.create_user(username=req_data['username'], email=req_data['email'],
                                            first_name=req_data['first_name'], last_name=req_data['last_name'])
            user.set_password(request.POST['password_confirm'])
            user.save()
            auth.login(request, user)
            return redirect('/')
    return render(request, 'registration.html', {'form': form, 'error_message': errors})


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('next', '/'))


@login_required(login_url='/login/')
def settings(request):
    if request.method == 'GET':
        form = SettingsForm(initial={'username': request.user.username,
                                     'email': request.user.email}, user=request.user)
    else:
        form = SettingsForm(data=request.POST, files=request.FILES, user=request.user)
        print(request.FILES)
        if form.is_valid():
            for change in form.changed_data:
                print(change)
                if change == 'avatar':
                    print("request.FILES[change]")
                    setattr(request.user, change, request.FILES[change])
                else:
                    setattr(request.user, change, request.POST[change])
            request.user.save()
            return redirect('settings')
    return render(request, 'settings.html', {'form': form})


def tag(request, tag):
    question = paginate(Tag.objects.question_by_tag(tag), request)
    return render(request, 'tag.html', {'questions': question, "tag": tag})
