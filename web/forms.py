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

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class TaskTagForm(forms.ModelForm):

    def save(self, commit = True):
        self.instance.user = self.initial['user']
        return super().save(commit)

    class Meta:
        model = TaskTag
        fields = ('title',)

    def __init__(self, *args, **kwargs):
        super(TaskTagForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})


class TaskFilterForm(forms.Form):
    search = forms.CharField(label = '', widget = forms.TextInput(
        attrs = {"placeholder": "Поиск", "class": "search-input"}), required = False)
    description = forms.TextInput()


class ImportForm(forms.Form):
    file = forms.FileField()
