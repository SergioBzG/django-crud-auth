from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# These is a class that Django provides to create a form for user creation (register) and user authentication
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# This is a class that Django provides to create users
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate # This (login) fuctionality allow create Cookies with login information user
from django.db import IntegrityError # This error is arised when the unique constraint in the db is violated
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required # This decorator allow to restrict access to a view if the user is not logged in

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
                username, password =  request.POST['username'], request.POST['password1']
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
    
@login_required
def tasks(request):
    # List pending tasks by a specific user
    tasks = Task.objects.filter(user_id=request.user.id, date_completed__isnull=True) 
    # tasks = Task.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required
def tasks_completed(request):
    # List completed tasks by a specific user
    tasks = Task.objects.filter(user_id=request.user.id, date_completed__isnull=False).order_by('-date_completed')
    # tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    # task = Task.objects.get(pk=task_id)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        try:
            # Using the TaskForm to update the task
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': 'Error updating task '
            })
        
@login_required
def completed_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.date_completed = timezone.now()
        task.save()
        return redirect('tasks')
    
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm 
        })
    else:
        try:
            # I can create a task using the model Taks or using the TaskForm class:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False) # commit=False means that the object is not saved in the db

            # Using request.user I can access to user info who is requesting the url
            new_task.user = request.user
            new_task.save()

            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Please provide a valid data'
            })

@login_required
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
    
