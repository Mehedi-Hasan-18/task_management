from django.urls import path
from tasks.views import dash_board,test,employee_dashboard,dashboard,CreateTask,ViewProject,TaskDetailView,UpdateTaskView,DeleteTaskView

urlpatterns = [
    path('dash_board/',dash_board, name="manager-dashboard"),
    path('employee_dashboard/',employee_dashboard, name="employee_dashboard"),
    path('test/',test),
    path('create_task/',CreateTask.as_view(), name="create-task"),
    path('task/<int:task_id>/details', TaskDetailView.as_view(), name='task-details'),
    path('view_task/',ViewProject.as_view(), name='view-task'), 
    path('update-task/<int:id>/',UpdateTaskView.as_view(), name="update-task"),  
    path('delete-task/<int:id>/',DeleteTaskView.as_view(), name="delete-task"),
    path('dashboard/', dashboard, name='dashboard')
]
