from distutils.util import strtobool

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from rabbit.forms import PostForm, LinkPostForm, ImgPostForm, WarrenForm, CommentForm
from rabbit.models import Post, Warren, Follower, Comment, Subscribe, Score

# Create your views here.
from rabbit.tree import Node


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
        warrens = Warren.objects.all()
        context["warrens"] = warrens
        context["warren"] = w
        context["posts"] = Post.objects.filter(warren=w.name).order_by('-creation_date')[:30]
        if request.user.is_authenticated:
            subscribing = get_subscribing(request.user)
            context['suscribing'] = [warren for warren in warrens if subscribing.filter(subscribing=warren)]
        return render(request, 'warren_view.html', context)

    except:
        return redirect(index)


def profile(request, name):
    context = {}
    try:
        r = User.objects.get(username=name)
        users = User.objects.all()
        warrens = Warren.objects.all()
        context["warrens"] = warrens
        context["user"] = r
        context["posts"] = Post.objects.filter(user=r).order_by('-creation_date')[:30]
        if request.user.is_authenticated:
            following = get_following(request.user)
            context['following'] = [user for user in users if following.filter(following=user)]
        return render(request, 'user_profile.html', context)
    except:
        return redirect(index)


@login_required()
def create_warren(request):
    context = {}
    if request.method == "POST":
        form = WarrenForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            w = form.save(commit=False)
            w.creator = request.user
            w.save()
            return redirect(warren, w.name)
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
    context = {'warrens': Warren.objects.all()}
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
        result_p = Post.objects.filter(Q(title__contains=query) | Q(warren__name__contains=query) |
                                       Q(link__contains=query))
    else:
        return index(request)
    context = {
        'lastPost': result_w,
        'users': result_u,
        'warrens': Warren.objects.all(),
        'posts': result_p
    }
    if request.user.is_authenticated:
        following = get_following(request.user)
        subscribing = get_subscribing(request.user)
        context['following'] = [user for user in result_u if following.filter(following=user)]
        context['suscribing'] = [warren for warren in result_w if subscribing.filter(subscribing=warren)]
    return render(request, 'search.html', context)


@login_required()
def delete(request, id):

    post = get_object_or_404(Post, id=id)
    if request.method == "POST" and request.user.is_authenticated\
            and request.user.id == post.user.id:
        post.delete()
        return JsonResponse(status='200', data={'status': 'ok'})
    context = {
        "post": post
    }
    return JsonResponse(status='200', data={'status': 'error', 'message': 'You can not delete this post.'})


@login_required()
def follow(request):
    if request.method == "POST":
        try:
            user1 = User.objects.get(username=request.POST["username"])
            user = User.objects.get(username=request.user.username)
            follower = user.following.filter(following=user1)
            if user == user1:
                return JsonResponse(status='200', data={'status': 'error', 'message': 'You can not follow yourself'})
            if follower:
                follower.delete()
            else:
                user.following.add(Follower(following=user1), bulk=False)
            return JsonResponse(status='200', data={'status': 'ok'})
        except Exception as ex:
            return JsonResponse(status='200', data={'status': 'error', 'message': str(ex)})


def get_following(user):
    return user.following.all()


def make_tree(all_comments, c, parent):
    n = Node(c, parent)
    for com in all_comments.filter(parent=c):
        make_tree(all_comments, com, n)


def post_view(request, id_post):
    post = get_object_or_404(Post, id=id_post)
    all_comments = post.comments.all()
    order = "New"
    if request.method == "POST":
        order = request.POST['drop1']

    if order == "Old":
        all_comments = all_comments.order_by('creation_date')
    elif order == "New":
        all_comments = all_comments.order_by('-creation_date')
    else:
        all_comments = all_comments.annotate(likes=Count('scores', filter=Q(scores__value=True)) -
                                             Count('scores', filter=Q(scores__value=False))).order_by('-likes')

    root = Node(None, None)
    for c in all_comments.filter(parent=None):
        make_tree(all_comments, c, root)
    users = User.objects.all()
    warrens = Warren.objects.all()
    context = {
        'post': post,
        'post_comments': root,
        'comment_form': CommentForm(),
        'warrens': warrens

    }
    if request.user.is_authenticated:
        following = get_following(request.user)
        subscribing = get_subscribing(request.user)
        context['following'] = [user for user in users if following.filter(following=user)]
        context['suscribing'] = [warren for warren in warrens if subscribing.filter(subscribing=warren)]
    return render(request, 'post.html', context)


@login_required()
def comment(request, id_post, id_comment=None):
    post = get_object_or_404(Post, id=id_post)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            com = form.save(commit=False)
            com.user = request.user
            com.post = post
            if id_comment:
                parent = get_object_or_404(Comment, id=id_comment)
                com.parent = parent
            com.save()
            return redirect(post_view, id_post=id_post)
        return JsonResponse(status='200', data={'status': 'error', 'message': form.errors})
    return JsonResponse(status='200', data={'status': 'error', 'message': 'only post page'})


@login_required()
def subscribe(request):
    if request.method == "POST":
        try:
            warren = Warren.objects.get(name=request.POST["name"])
            user = User.objects.get(username=request.user.username)
            subscriber = user.subscribing.filter(subscribing=warren)
            if subscriber:
                subscriber.delete()
            else:
                user.subscribing.add(Subscribe(subscribing=warren), bulk=False)
            return JsonResponse(status='200', data={'status': 'ok'})
        except Exception as ex:
            return JsonResponse(status='200', data={'status': 'error', 'message': str(ex)})


def get_subscribing(user):
    return user.subscribing.all()


@login_required()
def vote(request, id_post, id_comment=None):
    if request.method == "POST":
        if request.POST["score"] == "True" or request.POST["score"] == "False":
            post = get_object_or_404(Post, id=id_post)
            if id_comment:
                com = get_object_or_404(Comment, id=id_comment)
                score = com.scores.filter(user=request.user)
            else:
                com = None
                score = post.scores.filter(user=request.user)

            value = strtobool(request.POST["score"])
            if score:
                score = score[0]
                if score.value == value:
                    score.delete()
                else:
                    score.value = value
                    score.save()
            else:
                score = Score(post=post, user=request.user, value=value)
                score.comment = com
                score.save()
            return JsonResponse(status='200', data={'status': 'ok'})
        return JsonResponse(status='200', data={'status': 'error', 'message': 'Not valid Value'})
    return JsonResponse(status='200', data={'status': 'error', 'message': 'GET method not supported'})