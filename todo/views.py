from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm , UserCreateForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):

    return render(request, 'todo/home.html', {})

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreateForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)

                return redirect('currenttodos')
            except IntegrityError:
                error = {'This username has already been taken. Please choose a new username'}
                return render(request, 'todo/signupuser.html', {'form': UserCreateForm(), 'error':error})
        else:
            error = {'The passwords did not match'}
            return render(request, 'todo/signupuser.html', {'form': UserCreateForm(), 'error':error})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})  
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            error = {'Username and Password did not match'}
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':error})
            
        else:
            login(request, user)

            return redirect('currenttodos')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('loginuser')

    return render(request, 'todo/logoutuser.html', {})

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        
        # form = TodoFrom(request.POST or None)
        form = TodoForm(request.POST)
        new_todo = form.save(commit=False)
        new_todo.user = request.user
        new_todo.save()

        return redirect('currenttodos')
# def createtodo(request):
#     if request.method == 'GET':
#         return render(request, 'todo/createtodo.html', {'form':TodoForm()})
#     else:
#         try:
#             # form = TodoFrom(request.POST or None)
#             form = TodoForm(request.POST)
#             new_todo = form.save(commit=False)
#             new_todo.user = request.user
#             new_todo.save()
#         except ValueError:
#             return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error':'Bad data passed in. Try again.'})

#         return redirect('currenttodos')

@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)

    return render(request, 'todo/currenttodos.html', {'todos':todos})

@login_required    
def viewtodo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            # return redirect('viewtodo', pk=pk) # Stays on the same page
            return redirect('currenttodos')
        except ValueError:
            error = {'Bad data passed in. Try again.'}
            return render(request, 'todo/viewtodo.html', {'form':TodoForm(), 'error':error})

@login_required
def completetodo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    if todos.count() == 0:
        prompt = {"No todo is completed!"}
        return render(request, 'todo/completedtodos.html', {'prompt':prompt})

    return render(request, 'todo/completedtodos.html', {'todos':todos})