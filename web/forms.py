from django import forms
from django.contrib.auth import get_user_model

from web.models import Task, TaskTag

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(widget = forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            self.add_error("password", "Пароли не совпадают")
        return cleaned_data

    class Meta:
        model = User
        fields = ("email", "username", "password", "password2")


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput())


class TaskForm(forms.ModelForm):

    def save(self, commit = True):
        self.instance.user = self.initial['user']
        return super().save(commit)

    class Meta:
        model = Task
        fields = ('title', 'description', "image", "tags")


class TaskTagForm(forms.ModelForm):

    def save(self, commit = True):
        self.instance.user = self.initial['user']
        return super().save(commit)

    class Meta:
        model = TaskTag
        fields = ('title', )


class TaskFilterForm(forms.Form):
    search = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "Поиск"}), required=False)
    description = forms.TextInput()


class ImportForm(forms.Form):
    file = forms.FileField()