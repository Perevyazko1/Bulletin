from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post
from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm


admin.site.register(Post, PostAdmin)

admin.site.site_title = 'Админ панель Доска объявлений'
admin.site.site_header = 'Админ панель Доска объявлений'
