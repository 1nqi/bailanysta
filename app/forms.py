from django import forms
from .models import Khabar, Profile, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(required=False, label="Profile Picture")
    profile_bio = forms.CharField(required=False, label="Profile Bio", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Profile Bio'}))
    github_link =  forms.CharField(required=False, label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Github Link'}))
    instagram_link = forms.CharField(required=False, label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Instagram Link'}))
    telegram_link =  forms.CharField(required=False, label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Telegram Link'}))

    class Meta:
        model = Profile
        fields = ('profile_image', 'profile_bio',  'github_link', 'instagram_link', 'telegram_link', )



class KhabarForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        label='',
        widget=forms.Textarea(attrs={
            'placeholder': 'What\'s on your mind?',
            'rows': 3,
            'class': 'form-control'
        })
    )

    class Meta:
        model = Khabar
        exclude = ("user", "likes",)

class SignUpForm(UserCreationForm):
    username = forms.CharField(required=False, label='',
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Email Adress',
                                    'class': 'form-control'}))
    first_name = forms.CharField(required=False, label='', max_length=100, 
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'First Name',
                                    'class': 'form-control'}))
    last_name = forms.CharField(required=False, label='', max_length=100, 
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Last Name',
                                    'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class CommentForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        label='',
        widget=forms.Textarea(attrs={
            'placeholder': 'Write your comment...',
            'rows': 3,
            'class': 'form-control'
        })
    )

    class Meta:
        model = Comment
        fields = ('body',)

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(required=False, label='',
                              widget=forms.TextInput(attrs={
                                  'placeholder': 'Username',
                                  'class': 'form-control'}))
    email = forms.EmailField(required=False, label='',
                           widget=forms.EmailInput(attrs={
                               'placeholder': 'Email',
                               'class': 'form-control'}))
    first_name = forms.CharField(required=False, label='', max_length=100,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'First Name',
                                   'class': 'form-control'}))
    last_name = forms.CharField(required=False, label='', max_length=100,
                              widget=forms.TextInput(attrs={
                                  'placeholder': 'Last Name',
                                  'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')