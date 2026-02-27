from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='邮箱',
        widget=forms.EmailInput(attrs={
            'placeholder': '请输入邮箱',
            'id': 'id_email'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize field labels and placeholders
        self.fields['username'].label = '用户名'
        self.fields['username'].widget.attrs.update({
            'placeholder': '请输入用户名'
        })
        self.fields['password1'].label = '密码'
        self.fields['password1'].widget.attrs.update({
            'placeholder': '请输入密码'
        })
        self.fields['password2'].label = '确认密码'
        self.fields['password2'].widget.attrs.update({
            'placeholder': '请再次输入密码'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被注册')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('该用户名已存在')
        return username


class UserEditForm(forms.ModelForm):
    """Form for editing user information (admin only)"""
    email = forms.EmailField(
        required=True,
        label='邮箱',
        widget=forms.EmailInput(attrs={
            'placeholder': '请输入邮箱',
            'class': 'form-input'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
        labels = {
            'username': '用户名',
            'first_name': '名',
            'last_name': '姓',
            'is_active': '活跃状态',
            'is_staff': '管理员权限',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': '请输入用户名',
                'class': 'form-input'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': '请输入名',
                'class': 'form-input'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': '请输入姓',
                'class': 'form-input'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_id = self.instance.id if self.instance else None
        if User.objects.filter(email=email).exclude(id=user_id).exists():
            raise forms.ValidationError('该邮箱已被其他用户使用')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_id = self.instance.id if self.instance else None
        if User.objects.filter(username=username).exclude(id=user_id).exists():
            raise forms.ValidationError('该用户名已存在')
        return username