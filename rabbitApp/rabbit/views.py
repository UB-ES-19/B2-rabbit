from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import JsonResponse


# Create your views here.
def index(request):
    form = UserCreationForm()
    context = {
        'form': form
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

