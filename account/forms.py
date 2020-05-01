from django.contrib.auth.models import User
from django import forms

from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter First Name', 'label': ''}
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter Last Name', }
        )
    )
    password = forms.CharField(
         widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}
        ))
    password2 = forms.CharField(
         widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Repeat Password'}
        ))
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username'}
        ))
    email = forms.EmailField(
       widget=forms.EmailInput(
           attrs={'class': 'form-control', 'placeholder': 'Email'}
       ))

    class Meta:
        model = User
        fields = ('username','email','first_name', 'last_name',)
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError("Email already exist")

class ProfileForm(forms.ModelForm):
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'eg: +234 8030793112','label':''}
        )
    )
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter Address'}
        ), required=False,
    )

    class Meta:
        model = Profile
        fields = ('phone','address')



class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email','first_name', 'last_name',)

class ProfileEditForm(forms.ModelForm):
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'eg: +234 8030793112'}
        )
    )

    address = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter Address'}
        ), required=False
    )
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20})
                                  ,label='About', required=False)

    class Meta:
        model = Profile
        fields = ('phone', 'address', 'photo','date_of_birth',
                  'facebook','twitter','google','linkedin','description')

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs.update({'class': 'filestyle'})