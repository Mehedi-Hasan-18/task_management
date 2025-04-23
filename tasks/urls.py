from django.urls import path
from tasks.views import show_details

urlpatterns = [
    path('show_details/',show_details)
]
