from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from users.forms import RegisterForm,CustomRegisterForm,CustomSignInForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator

# Create your views here.
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