from django.urls import path
from tasks.views import dash_board,test,view_task,update_task,delete_task,task_details,employee_dashboard,dashboard,CreateTask,ViewProject,TaskDetailView,UpdateTaskView

urlpatterns = [
    path('dash_board/',dash_board, name="manager-dashboard"),
    path('employee_dashboard/',employee_dashboard, name="employee_dashboard"),
    path('test/',test),
    # path('create_task/',create_task, name="create-task"),
    path('create_task/',CreateTask.as_view(), name="create-task"),
    # path('task/<int:task_id>/details', task_details, name='task-details'),
    path('task/<int:task_id>/details', TaskDetailView.as_view(), name='task-details'),
    # path('create_task_prac/',create_task_prac),
    # path('view_task/',view_task, name='view-task'),
    path('view_task/',ViewProject.as_view(), name='view-task'),
    # path('update-task/<int:id>/',update_task, name="update-task"),  
    path('update-task/<int:id>/',UpdateTaskView.as_view(), name="update-task"),  
    path('delete-task/<int:id>/',delete_task, name="delete-task"),
    path('dashboard/', dashboard, name='dashboard')
]
