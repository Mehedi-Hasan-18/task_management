from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import re
from tasks.forms import styleMixin

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Fixed this line
    
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class CustomRegisterForm(styleMixin,forms.ModelForm): 
    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text="Must contain both letters and numbers (no special characters)"
    )
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email Already Exits")
        return email
        
    def clean_password(self):
        errors = []
        
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            errors.append("⋅ At least 8 characters")
        if not re.search(r'[A-Z]',password):
            errors.append("⋅ Password Must include one Upper case leter")
        if not re.search(r'[a-z]',password):
            errors.append("⋅ Password Must include one lower case leter") 
        if not re.search(r'[0-9]',password):
            errors.append("⋅ Password Must include one number") 
        if not re.search(r'[@#$%^$+=]',password):
            errors.append("⋅ Password Must include atleast one speacial character") 
        
        if errors:
            raise forms.ValidationError(errors)
            
        return password
    
    def clean(self):
        cleaned_data =  super().clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError('Password do not Match')
        
        return cleaned_data