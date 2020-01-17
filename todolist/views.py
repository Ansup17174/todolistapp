from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, update_session_auth_hash, get_user_model
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .forms import NewListForm, NewToDoForm, UserCreateForm
from .models import Todo, TodoList

# Create your views here.
def Index(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            for pk in list(request.POST.keys())[1:]:
                todo = get_object_or_404(Todo, pk=pk)
                todo.is_done = True
                todo.save()
            return HttpResponseRedirect(reverse('todolist:index'))
        else:
            user_todo_lists = user.todolist_set.all()
            for todolist in user_todo_lists:
                for todo in todolist.todo_set.all():
                    if not todo.is_done:
                        todolist.undone_todos = True
                        break
            return render(request, 'todolist/list.html', {'user_todo_lists': user_todo_lists})
    else:
        return render(request, 'todolist/not_logged.html')

def Register(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('todolist/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return render(request, 'todolist/account_created.html')
        else:
            errors = list(form.errors.values())
            return render(request, 'todolist/register.html', {'form': form, 'errors': errors})
    else:
        form = UserCreateForm()
        return render(request, 'todolist/register.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'todolist/account_activated.html')
    else:
        return render(request, 'todolist/invalid.html')

def DeleteToDo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.user == todo.todo_list.user:
        todo.delete()
        return HttpResponse(reverse('todolist:index'))
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

def TodoDone(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.user == todo.todo_list.user:
        todo.is_done = True
        todo.save()
        return HttpResponseRedirect(reverse('todolist:index'))
    else:
        return HttpResponse(status=404)

def PasswordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return render(request, 'todolist/password_changed.html')
        else:
            errors = list(form.errors.values())
            return render(request, 'todolist/password_change.html', {'form': form, 'errors': errors})
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'todolist/password_change.html', {'form': form})
