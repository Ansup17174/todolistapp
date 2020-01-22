from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class TodoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    list_title = models.CharField(max_length=25, default='list title')
    undone_todos = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.list_title

class Todo(models.Model):
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    todo_text = models.CharField(max_length=20, default='empty')
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.todo_text
