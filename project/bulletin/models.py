from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class PostCategory(models.Model):
    class Meta:
        verbose_name = u"Категория объявления"
        verbose_name_plural = u"Категории объявлений"

    name = models.CharField(max_length=100, unique=True, default=None)
    clients = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name


class Post(models.Model):
    class Meta:
        verbose_name = u"Объявление"
        verbose_name_plural = u"Объявления"

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    category = models.ForeignKey(
        to='PostCategory',
        on_delete=models.CASCADE,
        related_name='post',
        verbose_name='Категория'  # все продукты в категории будут доступны через поле news
    )

    title = models.CharField(max_length=128, verbose_name='Заголовок')
    text = RichTextUploadingField()
    response = models.ManyToManyField(User, related_name='rating')

    def total_response(self):
        return self.response.count()

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.title}| {self.text[:20]}'
