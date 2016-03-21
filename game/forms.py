from django import forms
from django.contrib.auth.models import User
from game import models

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class PlayerForm(forms.ModelForm):
    class Meta:
        model = models.Player
        fields = ('profile_picture',)
        widgets = {'games_played': forms.HiddenInput(), 'most_days_survived': forms.HiddenInput(), 'most_kills': forms.HiddenInput(),
                   'most_people': forms.HiddenInput(), 'current_game': forms.HiddenInput()}
