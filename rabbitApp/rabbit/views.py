from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from rabbit.forms import PostForm, LinkPostForm, ImgPostForm, WarrenForm
from rabbit.models import Post, Warren


# Create your views here.

def index(request):
    lastPost = Post.objects.order_by('-creation_date')[:30]
    warrens = Warren.objects.all()
    context = {
        'lastPost': lastPost,
        'warrens': warrens
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


def warren(request, name):
    context = {}
    try:
        w = Warren.objects.get(name=name)
        context["warren"] = w
        return render(request, 'warren_view.html', context)

    except:
        return redirect(index)


def profile(request, name):
    context = {}
    try:
        r = User.objects.get(username=name)
        posts = Post.objects.filter(user=r, warren=None).order_by('-creation_date')[:30]
        context["user"] = r
        context["posts"] = posts
        return render(request, 'user_profile.html', context)
    except:
        return redirect(index)


@login_required()
def create_warren(request):
    context = {}
    if request.method == "POST":
        form = WarrenForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user
            post.save()
            # Redirect a la pagina del warren, no está hecha aún :)
            return redirect(index)
        else:
            context["form_warren"] = form
            return render(request, 'warren.html', context)
    else:
        context["form_warren"] = WarrenForm()
        return render(request, 'warren.html', context)


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
            context["form_img_post"] = ImgPostForm()
            context['form_link'] = LinkPostForm()
            return render(request, 'postForm.html', context)
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
            return render(request, 'postForm.html', context)


@login_required()
def post_link(request):
    context = {}
    if request.method == "POST":
        form = LinkPostForm(request.POST)
        if form.is_valid():
            link_post = form.save(commit=False)
            link_post.user = request.user
            link_post.save()
            return JsonResponse(status='200', data={'status': 'ok'})
        else:
            context["form_link"] = form
            context["form_post"] = PostForm()
            context["form_img_post"] = ImgPostForm()
            return render(request, 'postForm.html', context)


@login_required()
def logout_user(request):
    logout(request)
    return redirect('/')

def search(request):
    query = request.GET.get('q')
    if query:
        result_w = Warren.objects.filter(Q(name__contains=query) | Q(description__contains=query))
        result_u = User.objects.filter(Q(username__contains=query))
    else:
        return index(request)
    context = {
        'lastPost': result_w,
        'users': result_u
    }
    return render(request, 'search.html', context)

@login_required()
def delete(request, id):

    post = get_object_or_404(Post, id=id)
    if request.method == "POST" and request.user.is_authenticated\
            and request.user.id == post.user.id:
        post.delete()
        return redirect('../../')
    context = {
        "post": post
    }
    return render(request, 'deletePost.html', context)
