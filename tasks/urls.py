from django.urls import path
from tasks.views import dash_board,test,create_task,create_task_prac

urlpatterns = [
    path('dash_board/',dash_board),
    path('test/',test),
    path('create_task/',create_task),
    path('create_task_prac/',create_task_prac)
]
