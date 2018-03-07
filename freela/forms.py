from django import forms
from django.forms import ModelForm
from freela.models import Project
from freela.models import Service

class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'Username',
        max_length = 32
    )
    email = forms.CharField(
        required = True,
        label = 'Email',
        max_length = 32,
    )
    password = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget = forms.PasswordInput()
    )

class ProjectRegistrationForm(forms.Form):
    name = forms.CharField(
        required = True,
        label = 'Name',
        max_length = 100,
        )
    budget = forms.IntegerField(
        required = True,
        label = 'Budget',
        )
    description = forms.CharField(
        required = True,
        label = 'Description',
        max_length = 1200,
        )

class EditProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'budget', 'description']

class EditServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'budget', 'description', 'area']

class ServiceRegistrationForm(forms.Form):
    name = forms.CharField(
        required = True,
        label = 'Name',
        max_length = 100,
        )
    budget = forms.IntegerField(
        required = True,
        label = 'Budget',
        )
    description = forms.CharField(
        required = True,
        label = 'Description',
        max_length = 1200,
        )
    area = forms.IntegerField(
        required = True,
        label = 'Area',
        )
    
class CommentRegistrationForm(forms.Form):
    text = forms.CharField(
        required = True,
        label = 'Text',
        max_length = 4000,
        )

