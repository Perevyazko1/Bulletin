from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView

from .forms import PostForm
from .models import Post, User


class Profile(ListView):
    raise_exception = True
    model = User
    template_name = 'profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user
        context['email'] = self.request.user.email
        # добавляем в контекст все доступные часовые пояса
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_id.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        news = get_object_or_404(Post, id=self.kwargs["pk"])
        # comment = get_object_or_404(Comment, id=self.kwargs["pk"])
        # total_likes_comment = comment.total_likes_comment()
        total_response = news.total_response()
        context['count'] = total_response
        # context['count_comment'] = total_likes_comment
        # context['comment'] = Comment.objects.filter(commentPost=self.kwargs["pk"])
        return context


class NewsList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'post.html'
    context_object_name = 'post'
    paginate_by = 10


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('bulletin.add_news',)
    raise_exception = True
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'edit_post.html'

    def form_valid(self, form):  # Переопределение метода при валидации формы NewsForm
        # print(self.request.user.id)

        self.object = form.save(commit=False
                                )  # object - экземпляр заполненной формы NewsForm из запроса POST. В БД не сохраняем
        self.object.author = User.objects.get(id=self.request.user.id)
        # Назначяем полю author модели News экзамеляр модели Author, где пользователь-автор совпадает с

        # пользователем-юзер
        return super().form_valid(
            form)
