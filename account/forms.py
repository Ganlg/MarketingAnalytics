from django import forms
from account.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'telephone', 'company',
            'address', 'city', 'postal', 'state', 'country', 'password', 'password2'
        )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            # self.fields[key].widget.attrs['class'] = 'form-control'
            if key in ['username', 'password', 'password2', 'email', 'company']:
                self.fields[key].widget.attrs['required'] = 'required'

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if password2 != password:
            raise forms.ValidationError("Inconsistent Password")

        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'Email has already been registered')
        return email


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, )
    password = forms.CharField(max_length=150, widget=forms.PasswordInput, required=True)


class ResetPasswordConfirmForm(forms.Form):
    password = forms.CharField(max_length=150, widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(max_length=150, widget=forms.PasswordInput, required=True)

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError("Inconsistent Password")
        return password2

