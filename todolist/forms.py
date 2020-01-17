from django import forms
from .models import TodoList, Todo
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
class NewListForm(forms.ModelForm):

    class Meta:
        model = TodoList
        fields = ('list_title',)
        exclude = ('user',)

class NewToDoForm(forms.ModelForm):

    class Meta:
        model = Todo
        fields = ('todo_text',)
        exclude = ('todo_list', 'is_done')


class UserCreateForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('email',)
