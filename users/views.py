from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from users.forms import RegisterForm,CustomRegisterForm
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def register(request):
    # form = RegisterForm()
    form = CustomRegisterForm()
    if request.method == 'POST':
        # form = RegisterForm(request.POST)
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'registers/register.html', {'form':form})

def signIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request,username=username,password=password)
        
        login(request,user)
        return redirect('home')
    
    return render(request,'registers/signin.html')
    
def signOut(request):
    if request.method == 'POST':
        logout(request)
        return redirect('signIn')
    return render(request,'home.html')