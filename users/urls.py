from django.urls import path
from users.views import register,signIn,signOut,active,admin_dashboard,assign_role,create_group,group_list
from tasks.views import task_details
urlpatterns = [
    path('register/',register, name='register'),
    path('signIn/',signIn, name='signIn'),
    path('logout/',signOut, name='signOut'),
    path('activate/<int:user_id>/<str:token>',active, name='active'),
    path('admin/dashboard',admin_dashboard, name='admin_dashboard'),
    path('admin/<int:user_id>/assignrole',assign_role, name='assign_role'),
    path('admin/create-group',create_group, name='create-group'),
    path('admin/group-list',group_list, name='group-list'),
]
