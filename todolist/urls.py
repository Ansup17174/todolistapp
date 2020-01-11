from django.urls import path
from . import views
app_name = 'todolist'
urlpatterns = [
    path('', views.Index, name='index'),
    path('register/', views.Register, name="register"),
    path('delete-todo/<int:pk>/', views.DeleteToDo, name='delete_todo'),
    path('delete-list-preview/<int:pk>/', views.DeleteListPreview, name='delete_list_preview'),
    path('delete-list/<int:pk>', views.DeleteList, name='delete_list'),
    path('new/', views.NewList, name='new_list'),
    path('new-todo/<int:pk>', views.NewToDo, name='new_todo'),
    path('edit-list/<int:pk>', views.EditList, name='edit_list'),
    path('edit-todo/<int:pk>', views.EditTodo, name='edit_todo'),
]
