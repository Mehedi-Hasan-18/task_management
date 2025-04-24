from django.urls import path
from tasks.views import dash_board,test

urlpatterns = [
    path('dash_board/',dash_board),
    path('test/',test)
]
