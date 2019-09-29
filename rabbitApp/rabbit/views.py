from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    return render(request, 'base.html')


def register(request):
    context = {
    }
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
        else:
            context["errors"] = form.errors

    return redirect(index, context)

def login(request):
    context = {}
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
            else:
                context["errors"] = form.errors

    return redirect(index, context)