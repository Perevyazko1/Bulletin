from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class AuthenticateForm(forms.Form):
    code = forms.UUIDField(label="code")

    # class Meta:
    #     # model = User
    #     fields = (
    #         "code",
    #     )


    # def clean(self):
    #     cleaned_data = super().clean()
    #     code = cleaned_data.get("code")
    #     if code is not None and len(code) < 36:
    #         raise ValidationError({
    #             "code": "Код авторизации должен выглядеть так ********-****-****-****-*************"
    #         })
    #
    #     # if title == text:
    #     #     raise ValidationError(
    #     #         "Описание не должно быть идентично названию."
    #     #     )
    #     #
    #     # if title is not None and len(title) > 128:
    #     #     raise ValidationError({
    #     #         "text": "Заголовок не может быть более 128 символов."
    #     #     })
    #
    #     return cleaned_data


# class PostForm(ModelForm):
#
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('prefix')
#         super(PostForm, self).__init__(*args, **kwargs)
#         user = User.objects.get(id=user.id)
#         self.fields['author'].initial = user.username
#
#     class Meta:
#         model = Post
#         fields = ['title', 'text', 'category']