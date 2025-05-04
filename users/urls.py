from django.urls import path
from users.views import register,signIn,signOut,active
urlpatterns = [
    path('register/',register, name='register'),
    path('signIn/',signIn, name='signIn'),
    path('logout/',signOut, name='signOut'),
    path('activate/<int:user_id>/<str:token>',active, name='active')
]
