import uuid

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class AuthUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4)
    authenticate = models.BooleanField(default=False)


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
    TANK = 'TNK'
    HILL = 'HL'
    DD = 'DD'
    MERCHANT = 'MRCH'
    GUILDMASTER = 'GMSTR'
    QUESTGIVER = 'QGVR'
    BLACKMITH = 'BLKMTH'
    TANNER = 'TNR'
    POTION = 'PTN'
    MASTER_SPELL = 'MSTRSPL'

    CATEGORY_CHOICES = (
        (TANK, 'Танк'),
        (HILL, 'Хилл'),
        (DD, 'ДД'),
        (MERCHANT, 'Торговец'),
        (GUILDMASTER, 'Гилдмастер'),
        (QUESTGIVER, 'Квестгивер'),
        (BLACKMITH, 'Кузнец'),
        (TANNER, 'Кожевник'),
        (POTION, 'Зельевар'),
        (MASTER_SPELL, 'Мастер заклинаний'),
    )

    category = models.CharField(
        max_length=128, choices=CATEGORY_CHOICES,
        default=TANK, verbose_name='Тип'
    )
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    text = RichTextUploadingField()

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.title}| {self.text[:20]}'


class Response(models.Model):
    class Meta:
        verbose_name = u"Комментарий к новости"
        verbose_name_plural = u"Комментарии к новостям"

    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Объявление')
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Отклик')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    status = models.BooleanField(default=False)

    def update_status(self):
        return Response.objects.filter(id=self.id).update(status=True)

    def __str__(self):
        return f'{self.dateCreation} {self.text} {self.commentUser}'
