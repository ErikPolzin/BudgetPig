from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def signup(request: HttpRequest) -> HttpResponse:
    """Create a new user."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})