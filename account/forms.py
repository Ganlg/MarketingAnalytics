from django import forms
from account.models import User

class RegisterForm(forms.ModelForm):
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
            self.fields[key].widget.attrs['class'] = 'form-control'
            if key in ['username', 'password', 'password2', 'email', 'company']:
                self.fields[key].widget.attrs['required'] = 'required'

    def clean_password2(self):
        if self.password2 != self.password:
            raise forms.ValidationError("Inconsistent Password")

        return self.password2


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, )
    password = forms.CharField(widget=forms.PasswordInput, required=True)

