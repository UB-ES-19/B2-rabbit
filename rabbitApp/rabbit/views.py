from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rabbit.forms import PostForm, LinkPostForm, ImgPostForm

# Create your views here.
from rabbit.models import Post


def index(request):
    context = {
    }
    return render(request, 'home.html', context)


def register(request):
    context = {
    }
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.save()
            return JsonResponse(status='200', data={'status': 'ok'})
        else:
            context["form_register"] = form
            return render(request, 'registrationForm.html', context)
    elif request.method == 'GET':
        form = UserCreationForm()
        context["form_register"] = form
        return render(request, 'registrationForm.html', context)


def login_user(request):
    context = {}
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse(status='200', data={'status': 'ok'})
            else:
                context['form_login'] = form
                return render(request, 'loginForm.html', context)
        else:
            return render(request, 'loginForm.html', {'form_login': form})
    elif request.method == "GET":
        form = AuthenticationForm()
        context["form_login"] = form
        return render(request, 'loginForm.html', context)


@login_required()
def create_post(request):
    context = {}
    if request.method == "POST":
        form = PostForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return JsonResponse(status='200', data={'status': 'ok'})
        else:
            context["form_post"] = form
            return render(request, 'submit.html', context)
    elif request.method == "GET":
        form = PostForm()
        context["form_post"] = form
        context["form_img_post"] = ImgPostForm()
        context['form_link'] = LinkPostForm()
        return render(request, 'submit.html', context)


@login_required()
def post_img(request):
    context = {}
    if request.method == "POST":
        form = ImgPostForm(request.POST, request.FILES)
        if form.is_valid():
            img_post = form.save(commit=False)
            img_post.user = request.user
            img_post.save()
            return JsonResponse(status='200', data={'status': 'ok'})
        else:
            context["form_post"] = PostForm()
            context["form_img_post"] = form
            context['form_link'] = LinkPostForm()
            return render(request, 'submit.html', context)


@login_required()
def post_link(request):
    context = {}
    if request.method == "POST":
        form = LinkPostForm(request.POST)
        if form.is_valid():
            img_post = form.save(commit=False)
            img_post.user = request.user
            img_post.save()
            return JsonResponse(status='200', data={'status': 'ok'})
        else:
            context["form_img_post"] = form
            context["form_post"] = PostForm()
            context["form_img_post"] = ImgPostForm()
            return render(request, 'submit.html', context)

