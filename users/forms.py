from django import forms
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Permission,Group
from events.forms import StyledFormMixin
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class CustomRegistrationForm(StyledFormMixin,forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        
    def clean_password(self):
        password = self.cleaned_data.get('password')
        errors = []
        if len(password) < 8:
            errors.append('Password must 8 character long')
        
        if not (re.search(r'[A-Z]', password) and 
                re.search(r'[a-z]', password) and 
                re.search(r'\d', password) and 
                re.search(r'[@#$%^&+=]', password)):
            errors.append('Password must include at least one uppercase letter, one lowercase letter, one number, and one special character')
            
        if errors:
            raise forms.ValidationError(errors)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password and confirm password didn't matched")
        return cleaned_data
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('The email is already taken!')
        return email
    
    
class LoginForm(StyledFormMixin,AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

class AssignRoleForm(StyledFormMixin,forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a role"
    )
    
class CreateGroupForm(StyledFormMixin,forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False,
        label = 'Assign Permission'
    )
    
    class Meta:
        model = Group
        fields = ['name','permissions']