from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.http import JsonResponse


# Create your views here.
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
            context["errors"] = form.errors
            context["form"] = form
            return render(request, 'registrationForm.html', {'form': form})
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
                return render(request, 'loginForm.html', {'form': form})
        else:
            return render(request, 'loginForm.html', {'form': form})
    elif request.method == "GET":
        form = AuthenticationForm()
        context["form_login"] = form
        return render(request, 'loginForm.html', context)
