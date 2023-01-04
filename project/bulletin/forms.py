from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=128)

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'category',

        ]

    # def clean(self):
    #     cleaned_data = super().clean()
    #     title = cleaned_data.get("title")
    #     text = cleaned_data.get("text")
    #
    #     if text is not None and len(text) < 10:
    #         raise ValidationError({
    #             "text": "Текст не может быть менее 10 символов."
    #         })
    #
    #     if title == text:
    #         raise ValidationError(
    #             "Описание не должно быть идентично названию."
    #         )
    #
    #     if title is not None and len(title) > 128:
    #         raise ValidationError({
    #             "text": "Заголовок не может быть более 128 символов."
    #         })
    #
    #     return cleaned_data


# class CommentNewsForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = [
#             'text',
#             # 'commentPost',
#             # 'commentUser',
#         ]
