from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Account, Profile
from django.utils.translation import ugettext_lazy as _


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = Account
        fields = ('username', 'password1', 'password2')


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', widget=forms.EmailInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Email or Password Incorrect!")


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ['is_active', 'is_staff', 'is_admin', 'is_superuser']

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Account.objects.exclude(
                    pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError(
                'Email "%s" is already in use.' % account)

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(
                    pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError(
                'Username "%s" is already in use.' % username)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        labels = {
            'account': _('User With This Profile:'),
            'first_name': _('First Name:'),
            'last_name': _('Last Name'),
            'profile_pic': _('Profile Picture:'),
            'document': _('Application Form:'),
        }
        widgets = {
            'account': forms.Select(attrs={'class': 'form-control', 'required': 'False'}),
        }
