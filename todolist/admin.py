from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreateForm, CustomUserChangeForm
from .models import CustomUser, TodoList, Todo
# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = UserCreateForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email']

admin.site.register(TodoList)
admin.site.register(Todo)
admin.site.register(CustomUser)