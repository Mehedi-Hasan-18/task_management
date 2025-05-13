from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import Group,Permission
from django import forms
import re
from tasks.forms import StyleFormMixin
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Fixed this line
    
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class CustomRegisterForm(StyleFormMixin,forms.ModelForm): 
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
    
    
class CustomSignInForm(StyleFormMixin,AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
class AssignRoleForm(StyleFormMixin,forms.Form):
    role = forms.ModelChoiceField(
        queryset= Group.objects.all(),
        empty_label= 'Selete Role--'
    )
    
class CreateGroupForm(StyleFormMixin,forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False,
        label = 'Assign Group' 
    )
    
    class Meta:
        model = Group
        fields = ['name', 'permissions']
        
class CustomPasswordChangeForm(StyleFormMixin, PasswordChangeForm):
    pass
class CustomPasswordResetForm(StyleFormMixin, PasswordResetForm):
    pass
class CustomPasswordResetConfirmForm(StyleFormMixin, SetPasswordForm):
    pass


"""class EditUserProfileForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        
    bio = forms.CharField(required=False, widget=forms.Textarea,label='bio')
    profile_img = forms.ImageField(required=False,label='Profile Image')
    
    def __init__(self,*args,**kwargs):
        self.userprofile = kwargs.pop('userprofile',None)
        super().__init__(*args,**kwargs)
        
        if self.userprofile:
            self.fields['bio'].initial = self.userprofile.bio
            self.fields['profile_img'].initial = self.userprofile.profile_img
            
    def save(self, commit=True):
        user = super().save(commit=False)
        
        if self.userprofile:
            self.userprofile.bio = self.cleaned_data.get('bio')
            self.userprofile.profile_img = self.cleaned_data.get('profile_img')

            if commit:
                self.userprofile.save()

        if commit:
            user.save()
        return user"""
        
        
class EditUserProfileForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email','last_name','first_name','bio','profile_img']