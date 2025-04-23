from django.contrib import admin
from django.urls import path,include
from tasks.views import home,contact,show_details

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home),
    path('contact/', contact),
    # path('show_details/',show_details),
    path('tasks/',include("tasks.urls"))
]
