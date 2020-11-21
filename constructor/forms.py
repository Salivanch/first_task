from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Profile, Question
from .send_msg import send


class RegistrationForm(UserCreationForm):
    email=forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Почта'}),label='',help_text="Введите вашу почту. На неё придет ссылка для подтверждения аккаунта.")

    def __init__(self, *args, **kwargs):
        super(RegistrationForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Логин'})
        self.fields['username'].label=""
        self.fields['password1'].widget.attrs.update({'placeholder': 'Пароль'})
        self.fields['password1'].label=""
        self.fields['password2'].widget.attrs.update({'placeholder': 'Пароль еще раз'})
        self.fields['password2'].label=""

    def clean_email(self):
        cleaned_data = super(RegistrationForm,self).clean() 
        email=cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с такой почтой уже существует.')
        return email

    class Meta:
        model=User
        fields=('username','password1','password2','email')
        

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Логин'}),label='', )
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Пароль'}),label='')

    def __init__(self,*args, **kwargs):
        self.domain=kwargs.pop('domain')
        super(LoginForm,self).__init__(*args,**kwargs)

    def clean(self):
        cleaned_data = super(LoginForm,self).clean() 
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user=authenticate(username=username, password=password)
        if not user:
            raise ValidationError('Пользователя с таким логином и паролем не существует.')
        profile=Profile.objects.get(user=User.objects.get(username=username))
        if profile:
            if not profile.confirmed:
                send(cleaned_data.get('username'),profile.user.email,self.domain)
                raise ValidationError(f'Для входа необходимо подтвредить почту. На почту {profile.user.email} был отправлена ссылка на подтвреждение аккаунта.')
        return cleaned_data

    class Meta:
        model=User
        fields=("username","password")


class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuestionForm,self).__init__(*args,**kwargs)
        self.fields['phone'].label_suffix=""
        self.fields['name'].label_suffix=""
        self.fields['email'].label_suffix=""

    class Meta:
        model=Question
        fields=('name','phone','email')