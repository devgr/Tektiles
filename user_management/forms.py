from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder
from crispy_forms.bootstrap import PrependedText, PrependedAppendedText, FormActions
from user_management.models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = '/user/login'
        self.helper.form_class = 'blueForms'
        self.helper.html5_required = True
        self.helper.add_input(Submit('submit', 'Submit'))

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()

        uname = cleaned_data.get('username')
        pw = cleaned_data.get('password')

        user = authenticate(username=uname, password=pw)
        if user is None:
            raise forms.ValidationError("Username and/or password is invalid")
        elif not user.is_active:
            raise forms.ValidationError("Your email has not yet been verified")

        cleaned_data['user'] = user
        return cleaned_data

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=15)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    matching_password = forms.CharField(widget=forms.PasswordInput(),
                                        label="Password (again)")

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = '/user/register'
        self.helper.form_class = 'blueForms'
        self.helper.html5_required = True
        self.helper.add_input(Submit('submit', 'Submit'))

    def clean_matching_password(self):
        pw1 = self.cleaned_data.get("password")
        pw2 = self.cleaned_data.get("matching_password")

        if not pw2:
            raise forms.ValidationError("You must confirm your password")
        elif pw1 != pw2:
            raise forms.ValidationError("Passwords do not match")

        return pw2

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    matching_password = forms.CharField(widget=forms.PasswordInput(),
                                        label='New password (again)')

    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.user = user
        self.helper = FormHelper()
        self.helper.form_action = '/user/change-password'
        self.helper.form_class = 'blueForms'
        self.helper.html5_required = True
        self.helper.add_input(Submit('submit', 'Submit'))

    def clean_old_password(self):
        pw = self.cleaned_data.get('old_password')
        user = authenticate(username=self.user.username, password=pw)

        if user is None:
            raise forms.ValidationError("Password is incorrect")

        return pw

    def clean_new_password(self):
        new_pw = self.cleaned_data.get('new_password')

        if len(new_pw) < 6 or not any(c.isupper() or c.isdigit() for c in new_pw):
            raise forms.ValidationError(
                '''Password must be at least six characters long and contain
                either an uppercase character or a number''')

        return new_pw

    def clean_matching_password(self):
        new_pw = self.data.get('new_password')
        matching_pw = self.cleaned_data.get('matching_password')

        if not matching_pw:
            raise forms.ValidationError('You must confirm your password')

        if new_pw != matching_pw:
            raise forms.ValidationError('Passwords do not match')

        return matching_pw


class EmailChangeForm(forms.ModelForm):
    email = forms.EmailField()
    current_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email',) # leave this comma - it is important!

    def __init__(self, *args, **kwargs):
        super(EmailChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = '/user/change-email'
        self.helper.form_class = 'blueForms'
        self.helper.html5_required = True
        self.helper.add_input(Submit('submit', 'Submit'))

    def clean_current_password(self):
        pw = self.cleaned_data.get('current_password')
        user = authenticate(username=self.instance.username, password=pw)

        if user is None:
            raise forms.ValidationError('Password is incorrect')

        return pw

class ContactForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'email')
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper.form_tag = False
        self.helper = FormHelper()
        self.helper.form_id = 'id-contact-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = '/contact/'
        self.helper.add_input(Submit('submit', 'Submit'))
