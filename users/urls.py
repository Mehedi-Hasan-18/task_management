from django.urls import path
from users.views import admin_dashboard,group_list,CustomLoginView,ProfileView,ChangePassword,CustomPasswordResetView,CustomPasswordReseConfirmtView,EditProfileView,RegisterView,AccountActivationView,CustomLogoutView,AssignRoleView,CreateGroupView
from django.contrib.auth.views import LogoutView,PasswordChangeDoneView


urlpatterns = [
    path('register/',RegisterView.as_view(), name='register'),
    path('signIn/',CustomLoginView.as_view(template_name='registers/signin.html'), name='signIn'),
    path('logout/',CustomLogoutView.as_view(), name='signOut'),
    path('activate/<int:user_id>/<str:token>/',AccountActivationView.as_view(), name='active'),
    path('admin/dashboard/',admin_dashboard, name='admin_dashboard'),
    path('admin/<int:user_id>/assignrole/',AssignRoleView.as_view(), name='assign_role'),
    path('admin/create-group/',CreateGroupView.as_view(), name='create-group'),
    path('admin/group-list/',group_list, name='group-list'),
    path('profile/',ProfileView.as_view(template_name='accounts/profile.html'), name='profile' ),
    path('change-password/', ChangePassword.as_view(), name='change_password' ),
    path('change-password/done/', PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done/' ),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset' ),
    path('password-reset/confirm/<uidb64>/<token>', CustomPasswordReseConfirmtView.as_view(), name='password_reset_confirm' ),
    path('edit-profile', EditProfileView.as_view(), name='edit_profile')
]
