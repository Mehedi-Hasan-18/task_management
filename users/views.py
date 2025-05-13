from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from users.forms import RegisterForm,CustomRegisterForm,CustomSignInForm,AssignRoleForm,CreateGroupForm,CustomPasswordChangeForm,CustomPasswordResetForm,CustomPasswordResetConfirmForm,EditUserProfileForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.views import LoginView,PasswordChangeDoneView,PasswordChangeView,PasswordResetView,PasswordResetConfirmView
from django.views.generic import TemplateView,UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

User = get_user_model()
"""from users.models import UserProfile"""

# Create your views here.

"""class EditProfileView(UpdateView):
    model = User
    form_class = EditUserProfileForm
    template_name = 'accounts/edit_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user
    
    def get_form_kwargs(self):
        kwargs =  super().get_form_kwargs()
        kwargs['userprofile'] = UserProfile.objects.get(user = self.request.user)
        return kwargs

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user = self.request.user)
        context['form'] = self.form_class(instance = self.object,userprofile = user_profile)
        return context
    
    def form_valid(self, form):
        form.save(commit=True)
        return redirect('profile')"""
        
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


def register(request):
    # form = RegisterForm()
    form = CustomRegisterForm()
    if request.method == 'POST':
        # form = RegisterForm(request.POST)
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False
            user.save()
            
            messages.success(request,"Please Varify Your Emali")
            return redirect('signIn')
    return render(request, 'registers/register.html', {'form':form})

class CustomLoginView(LoginView):
    form_class = CustomSignInForm
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()
  
class ChangePassword(PasswordChangeView):
    template_name='accounts/password_change.html'
    form_class = CustomPasswordChangeForm


def signIn(request):
    # form = AuthenticationForm()
    form = CustomSignInForm()
    if request.method == 'POST':
        # form = AuthenticationForm(request,data=request.POST)
        form = CustomSignInForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
    
    return render(request,'registers/signin.html', {'form':form})
    
def signOut(request):
    if request.method == 'POST':
        logout(request)
        return redirect('signIn')
    return render(request,'home.html')

@login_required
def active(request,user_id,token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            return redirect('signIn')
        else:
            return HttpResponse("INVALID USERNAME OR TOKEN")
    except User.DoesNotExist:
        return HttpResponse("USER DOES NOT EXIST")
    
@user_passes_test(is_admin,login_url='no-permission')    
def admin_dashboard(request):
    users = User.objects.prefetch_related('groups').all()
    
    for user in users:
        if user.groups.exists():
            user.group_name = user.groups.first().name
        else:
            user.group_name = 'NO Group Assign'
        
    return render(request,'admin/dashboard.html', {'users':users})

@user_passes_test(is_admin,login_url='no-permission')  
def assign_role(request,user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f'Role Changed Done for {user.username}')
            return redirect('admin_dashboard')
    return render(request, 'admin/assign_role.html', {'form':form})

@user_passes_test(is_admin,login_url='no-permission')  
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success = f'Group Created SuccessFul'
        return redirect('admin_dashboard')
    return render(request,'admin/create_group.html', {'form':form})

@user_passes_test(is_admin,login_url='no-permission') 
def group_list(request):
    groups = Group.objects.prefetch_related('permissions')
    return render(request,'admin/group_list.html', {'groups':groups})



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
    