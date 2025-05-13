from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from users.forms import RegisterForm,CustomRegisterForm,CustomSignInForm,AssignRoleForm,CreateGroupForm,CustomPasswordChangeForm,CustomPasswordResetForm,CustomPasswordResetConfirmForm,EditUserProfileForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from django.contrib.auth.views import LoginView,PasswordChangeDoneView,PasswordChangeView,PasswordResetView,PasswordResetConfirmView,LogoutView
from django.views.generic import TemplateView,UpdateView,CreateView,View,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

User = get_user_model()
        
class EditProfileView(UpdateView):
    model = User
    form_class = EditUserProfileForm
    template_name = 'accounts/edit_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save(commit=True)
        return redirect('profile')
    

# test function
def is_admin(user):
    return user.groups.filter(name='Admin').exists()


class RegisterView(CreateView):
    form_class = CustomRegisterForm
    template_name='registers/register.html'
    success_url = reverse_lazy('signIn')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password'))
        user.is_active = False
        user.save()
        
        messages.success(self.request,"Please Varify Your Emali")
        return super().form_valid(form)
    
    
    def get(self,request,*args, **kwargs):
        form = self.form_class()
        return self.render_to_response({'form':form})

class CustomLoginView(LoginView):
    form_class = CustomSignInForm
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()
 
class ChangePassword(PasswordChangeView):
    template_name='accounts/password_change.html'
    form_class = CustomPasswordChangeForm

@method_decorator(login_required, name='dispatch')
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('signIn')

 
class AccountActivationView(View):
    def get(self, request, user_id, token):
        try:
            user = User.objects.get(id=user_id)
      
            if not default_token_generator.check_token(user, token):
                messages.error(request, "Invalid activation link")
                return redirect('signIn')
                
            user.is_active = True
            user.save()
            
            messages.success(request, "Account activated successfully! You can now login")
            return redirect('signIn')
            
        except User.DoesNotExist:
            messages.error(request, "User does not exist")
            return redirect('signIn')
    
@user_passes_test(is_admin,login_url='no-permission')    
def admin_dashboard(request):
    users = User.objects.prefetch_related('groups').all()
    
    for user in users:
        if user.groups.exists():
            user.group_name = user.groups.first().name
        else:
            user.group_name = 'NO Group Assign'
        
    return render(request,'admin/dashboard.html', {'users':users})


@method_decorator(permission_required(is_admin,login_url='signIn'), name='dispatch')
class AssignRoleView(FormView):
    form_class = AssignRoleForm
    template_name = 'admin/assign_role.html'
    success_url = reverse_lazy('admin_dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(id=self.kwargs['user_id'])
        return context
    
    def form_valid(self, form):
        user = User.objects.get(id=self.kwargs['user_id'])
        role = form.cleaned_data.get('role')
        user.groups.clear()
        user.groups.add(role)
        messages.success(self.request, f'Role changed for {user.username}')
        return super().form_valid(form)
    

@method_decorator(permission_required(is_admin,login_url='signIn') ,name='dispatch')
class CreateGroupView(CreateView):
    form_class = CreateGroupForm
    template_name = 'admin/create_group.html'
    success_url = reverse_lazy('admin_dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Group Created Successfully')
        return response
    

@user_passes_test(is_admin,login_url='no-permission') 
def group_list(request):
    groups = Group.objects.prefetch_related('permissions')
    return render(request,'admin/group_list.html', {'groups':groups})


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        user = self.request.user
        
        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['bio'] = user.bio
        context['profile_img'] = user.profile_img
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        
        return context
    
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registers/reset_password.html'
    success_url = reverse_lazy('signIn')
    html_email_template_name = 'registers/reset_email.html'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context
    
    def form_valid(self, form):
        messages.success(self.request,'A password Reset Email Send')
        return super().form_valid(form)

class CustomPasswordReseConfirmtView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registers/reset_password.html'
    success_url = reverse_lazy('signIn')
    
    
    def form_valid(self, form):
        messages.success(self.request,'Password Reset SuccessFully')
        return super().form_valid(form)
    