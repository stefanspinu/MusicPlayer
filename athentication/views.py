from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm, RegistrationForm
# Create your views here.


def login_request(request):
    title = 'Login'
    form = UserLoginForm(request.POST or None)

    context = {
        'form': form,
        'title': title
    }

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)

        login(request, user)
        return redirect('home')
    else:
        print(form.errors)
    return render(request, 'authentication/login.html', context)


def signup_request(request):
    title = 'Create account'
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    context = {
        'form': form,
        'title': title
    }
    return render(request, 'authentication/singup.html', context)


def logout_request(request):
    logout(request)
    return redirect('login')
