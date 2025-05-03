from django.urls import path
from users.views import register,signIn,signOut
urlpatterns = [
    path('register/',register, name='register'),
    path('signIn/',signIn, name='signIn'),
    path('logout/',signOut, name='signOut')
]
