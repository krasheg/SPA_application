from django import forms

from captcha.fields import CaptchaField


class NewComment(forms.Form):
    user_name = forms.CharField(max_length=30, required=True, label="User Name",
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=50, required=True, label="E-mail",
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    home_page = forms.URLField(max_length=256, required=False, label="Home page",
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label="CAPTCHA")
    text = forms.CharField(max_length=1000, required=True, label="Text",
                           widget=forms.Textarea(attrs={'class': 'form-control'}))
    parent_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'class': 'visually-hidden'}), label=False)
    file = forms.FileField(label="Upload File", required=False)
    image = forms.ImageField(label="Upload Image", required=False)
