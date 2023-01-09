from django import forms

from .models import Post, Response


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=128)

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'category',

        ]


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = [
            'text',
        ]


class SendMailForm(forms.Form):
    text = forms.CharField(max_length=1128, widget=forms.Textarea)
