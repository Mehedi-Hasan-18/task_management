from django.urls import path
from tasks.views import show_details,show_specific_task

urlpatterns = [
    path('show_details/',show_details),
    path('show_details/<int:id>/',show_specific_task)
]
