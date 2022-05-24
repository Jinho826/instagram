from django import forms
from django.contrib.auth.forms import UserCreationForm
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
        fields = ['username', 'email', 'first_name', 'last_name','password1']
        labels = {
            'username' : '아이디',
            'password1' : '비밀번호',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("이미 등록된 이메일 주소입니다.")
        return email