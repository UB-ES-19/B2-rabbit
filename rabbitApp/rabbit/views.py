from django.contrib.auth.forms import UserCreationForm
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
