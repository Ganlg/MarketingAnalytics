from django import forms
from account.models import User

class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'telephone', 'company',
            'address', 'state', 'postal', 'country', 'password', 'password2'
        )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['class'] = 'form-control'
        # for visible in form.visible_fields():
        #     visible.field.widget.attrs['class'] = 'form-control'

    def clean_password2(self):
        if self.password2 != self.password:
            raise forms.ValidationError("Inconsistent Password")

        return self.password2