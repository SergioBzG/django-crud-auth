from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/completed', views.completed_task, name='completed_task'),
    path('tasks/completed', views.tasks_completed, name='tasks_completed'),
    path('tasks/<int:task_id>/delete', views.delete_task, name='delete_task'),
    path('logout/', views.signout, name='logout'),
    path('login/', views.signin, name='login'),
]