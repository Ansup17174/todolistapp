from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, HttpResponseRedirect, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import NewListForm, NewToDoForm
from .models import Todo, TodoList

# Create your views here.
def Index(request):
    user = request.user
    if user.is_authenticated:
        user_todo_lists = user.todolist_set.all()
        return render(request, 'todolist/list.html', {'user_todo_lists': user_todo_lists})
    else:
        return render(request, 'todolist/not_logged.html')

def Register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('todolist:index'))
        else:
            return HttpResponseRedirect(reverse('todolist:register'))
    else:
        form = UserCreationForm()
        return render(request, 'todolist/register.html', {'form': form})

def DeleteToDo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.user == todo.todo_list.user:
        todo.delete()
        return HttpResponseRedirect(reverse('todolist:index'))
    else:
        return HttpResponse(status=404)


def DeleteListPreview(request, pk):
    todolist = get_object_or_404(TodoList, pk=pk)
    if request.user == todolist.user:
        return render(request, 'todolist/list_delete.html', {'pk': pk})
    else:
        return HttpResponse(status=404)

def DeleteList(request, pk):
    todolist = get_object_or_404(TodoList, pk=pk)
    if request.user == todolist.user:
        todolist.delete()
        return HttpResponseRedirect(reverse('todolist:index'))
    else:
        return HttpResponse(status=404)

def NewList(request):
    if request.method == 'POST':
        form = NewListForm(request.POST)
        if form.is_valid():
            todolist = form.save(commit=False)
            todolist.user = request.user
            form.save()
            return HttpResponseRedirect(reverse('todolist:index'))
        else:
            return HttpResponseRedirect(reverse('todolist:new_list'))
    else:
        form = NewListForm(initial={'list_title': "{}'s list".format(request.user.username)})
        return render(request, 'todolist/new_list.html', {'form': form})

def NewToDo(request, pk):
    todolist = get_object_or_404(TodoList, pk=pk)
    if request.user == todolist.user:
        if request.method == 'POST':
            form = NewToDoForm(request.POST)
            if form.is_valid():
                todo = form.save(commit=False)
                todo.todo_list = get_object_or_404(TodoList, pk=pk)
                form.save()
                return HttpResponseRedirect(reverse('todolist:index'))
            else:
                return HttpResponseRedirect(reverse('todolist:new_todo', args=(pk,)))
        else:
            form = NewToDoForm(initial={'todo_text': ''})
            return render(request, 'todolist/new_todo.html', {'form': form})
    else:
        return HttpResponse(status=404)

def EditList(request, pk):
    todolist = get_object_or_404(TodoList, pk=pk)
    if request.user == todolist.user:
            if request.method == 'POST':
                form = NewListForm(request.POST, instance=todolist)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse('todolist:index'))
                else:
                    return HttpResponseRedirect(reverse('todolist:edit_list', args=(pk,)))
            else:
                form = NewListForm(instance=todolist, initial={'list_title': todolist.list_title})
                return render(request, 'todolist/new_list.html', {'form': form})
    else:
        return HttpResponse(status=404)

def EditTodo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.user == todo.todo_list.user:
        if request.method == 'POST':
            form = NewToDoForm(request.POST, instance=todo)
            if form.is_valid():
                todo = form.save(commit=False)
                todo.save()
                return HttpResponseRedirect(reverse('todolist:index'))
            else:
                return HttpResponseRedirect(reverse('todolist:edit_todo', args=(pk,)))
        else:
            form = NewToDoForm(instance=todo, initial={'todo_text': todo.todo_text})
            return render(request, 'todolist/new_todo.html', {'form': form})
    else:
        return HttpResponse(status=404)