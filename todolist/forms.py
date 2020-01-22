from django import forms
from .models import TodoList, Todo
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

