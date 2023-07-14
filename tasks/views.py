from django.shortcuts import render, redirect
from django.http import HttpResponse
# These is a class that Django provides to create a form for user creation (register) and user authentication
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# This is a class that Django provides to create users
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate # This (login) fuctionality allow create Cookies with login information user
from django.db import IntegrityError # This error is arised when the unique constraint in the db is violated

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm()
        })
    elif request.method == 'POST':
        print(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            # If someting goes wrong with db
            try:
                # Create user
                username, password =  str(request.POST['username']), str(request.POST['password1'])
                user = User.objects.create_user(username=username, password=password)
                # Save user
                user.email = request.POST['username']+'@unal.edu.co'
                user.save()

                # Create cookie with authentication info and open sesion
                login(request, user) 

                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm(),
                    'error': 'User already exists'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm(),
            'error': 'Passwords do not match'
        })
    

def tasks(request):
    return render(request, 'tasks.html')


def create_task(request):
    return render(request, 'create_task.html')


def signout(request):
    # Close sesion
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm()
        })
    else:
        # With the authenticate(request, username, password) we can verify if a user is valid
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm(),
                'error': 'username or password is incorrect'
            })
        # If user is valid her session is saved
        login(request, user)
        return redirect('tasks')
    
