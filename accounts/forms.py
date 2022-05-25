from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, PasswordChangeForm as AuthPasswordChangeForm
)
from .models import User

# class SignupForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password']    # 그대로 비밀번호가 들어감

class SignupForm(UserCreationForm):  # UserCreateionForm은 User모델을 기반으로 Form이 생김
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True  #필수필드
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'username' : '아이디',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("이미 등록된 이메일 주소입니다.")
        return email

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'website_url','bio', 'phone_number','gender','avatar']

class PasswordChangeForm(AuthPasswordChangeForm):
    def clean_new_password1(self):
        old_password = self.cleaned_data["old_password"]
        new_password1 = self.cleaned_data["new_password1"]
        if old_password and new_password1:
            if old_password == new_password1:
                raise forms.ValidationError("새로운 암호는 기존 암호과 다르게 입력해주세요.")
        return new_password1