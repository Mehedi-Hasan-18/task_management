from django.urls import path
from tasks.views import dash_board,test,create_task,view_task,update_task,delete_task,task_details,employee_dashboard,dashboard

urlpatterns = [
    path('dash_board/',dash_board, name="manager-dashboard"),
    path('employee_dashboard/',employee_dashboard, name="employee_dashboard"),
    path('test/',test),
    path('create_task/',create_task, name="create-task"),
    path('task/<int:task_id>/details', task_details, name='task-details'),
    # path('create_task_prac/',create_task_prac),
    path('view_task/',view_task),
    path('update-task/<int:id>/',update_task, name="update-task"),
    path('delete-task/<int:id>/',delete_task, name="delete-task"),
    path('dashboard', dashboard, name='dashboard')
]
