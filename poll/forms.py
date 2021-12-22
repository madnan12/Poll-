from django import forms
from django.db import models
from django.forms import ModelForm
from poll.models import Comments, Upload,Poll,Vote,Choice



class UsersForm(forms.Form):
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),

    ]

    username = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'signup-form-input', 'placeholder': 'enter your username'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'signup-form-input', 'placeholder': 'enter your email'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'signup-form-input password-field', 'placeholder': 'enter your password'}))
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'signup-form-input', 'placeholder': 'enter your first name'}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'signup-form-input', 'placeholder': 'enter your last name'}))
    profile_image = forms.FileField(widget=forms.FileInput(
        attrs={'class': 'signup-form-input', 'placeholder': 'enter your profile image'}))
    dob = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'signup-form-input', 'placeholder': 'enter your dob'}))
    gender = forms.ChoiceField(choices=gender_choices, widget=forms.RadioSelect(
        attrs={'class': 'option-input radio', 'placeholder': 'select gender'}))
    mobile_number = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'signup-form-input', 'placeholder': 'enter your mobile number'}))


class PostForm(forms.Form):
    content = forms.CharField(max_length=500, widget=forms.TextInput(
        attrs={'class': 'form-control'}))


class PostMediaForm(forms.Form):

    image = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'class': 'form-control'}))
    video = forms.FileField(required=False, widget=forms.FileInput(
        attrs={'class': 'form-control'}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']

        widgets = {
            'comment': forms.TextInput(attrs={'class': 'signup-form-input', 'rows': '5', 'placeholder': 'Say something...'})
        }


class AlbumPostForm(forms.Form):
    album_image = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'signup-form-input', 'placeholder': 'enter your profile image'}))
    album_video = forms.FileField(required=False, widget=forms.FileInput(
        attrs={'class': 'signup-form-input', 'placeholder': 'enter your profile image'}))
    content = forms.CharField(max_length=200, required=False, widget=forms.TextInput(
        attrs={'class': 'signup-form-input', 'placeholder': 'content(optional)'}))
    name = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'class': 'signup-form-input', 'placeholder': 'Album name'}))


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ('nameImage', 'uploadedImage')
        widgets = {
            'nameImage': forms.TextInput(attrs={'class': "login-form-input", 'placeholder': 'Enter image name'}),
            'uploadedImage': forms.FileInput(attrs={'class': "login-form-input"})
        }


class ThumbnailForm(forms.Form):
    
    video=forms.FileField(widget=forms.FileInput(
        attrs={'class': 'signup-form-input', 'placeholder': 'enter your profile image'}))

class PollAddForm(forms.ModelForm):

    choice1 = forms.CharField(label='Choice 1', max_length=100, min_length=2,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    choice2 = forms.CharField(label='Choice 2', max_length=100, min_length=2,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    choice3 = forms.CharField(label='Choice 3', max_length=100, min_length=2,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Poll
        fields = ['text', 'choice1', 'choice2','choice3']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
        }


class EditPollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['text', ]
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
        }


class ChoiceAddForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text', ]
        widgets = {
            'choice_text': forms.TextInput(attrs={'class': 'form-control', })
        }

    