from django.urls import path
from django.conf.urls import url
from . import views
app_name = 'todolist'
urlpatterns = [
    path('', views.Index, name='index'),
    path('register/', views.Register, name="register"),
    path('delete-todo/<int:pk>/', views.DeleteToDo, name='delete_todo'),
    path('delete-list/<int:pk>', views.DeleteList, name='delete_list'),
    path('new/', views.NewList, name='new_list'),
    path('new-todo/<int:pk>', views.NewToDo, name='new_todo'),
    path('edit-list/<int:pk>', views.EditList, name='edit_list'),
    path('edit-todo/<int:pk>', views.EditTodo, name='edit_todo'),
    path('todo-done/<int:pk>', views.TodoDone, name='todo_done'),
    path('password_change/', views.PasswordChange, name='password_change'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_account, name='activate'),
]
