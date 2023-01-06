from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from .forms import PostForm, ResponseForm
from .models import Post, User, Response


class Profile(ListView):
    raise_exception = True
    model = User
    template_name = 'profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        author = User.objects.get(id=self.request.user.id)
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user
        context['email'] = self.request.user.email
        context['post'] = Post.objects.filter(author=author)
        # добавляем в контекст все доступные часовые пояса
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_id.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        post = get_object_or_404(Post, id=self.kwargs["pk"])
        # comment = get_object_or_404(Comment, id=self.kwargs["pk"])
        # total_likes_comment = comment.total_likes_comment()
        total_like = post.total_like()
        context['count'] = total_like
        # context['count_comment'] = total_likes_comment
        # context['comment'] = Comment.objects.filter(commentPost=self.kwargs["pk"])
        return context


class PostList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'post.html'
    context_object_name = 'post'
    paginate_by = 10


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('bulletin.add_news',)
    raise_exception = True
    form_class = PostForm
    model = Post
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


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('bulletin.change_news',)
    form_class = PostForm
    model = Post
    template_name = 'edit_post.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('bulletin.delete_news',)
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('post_list')


@login_required  # проверка зареган ли user
def like_post(request, pk):
    n = Post.objects.get(id=pk)
    u = User.objects.get(id=request.user.id)
    if n.like.filter(id=u.id).exists():
        n.like.remove(u)
    else:
        n.like.add(u)
    return redirect(reverse('post_detail', args=[str(pk)]))


class ResponseCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = ResponseForm
    model = Response
    template_name = 'response.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.commentUser = User.objects.get(
            username=self.request.user)
        self.object.commentPost = Post.objects.get(
            id=self.kwargs["pk"])
        return super().form_valid(
            form)


@login_required  # проверка зареган ли user
def user_response(request, pk):
    user = request.user
    post = Post.objects.get(id=pk)
    response = Response.objects.filter(commentPost=post,commentUser=user)

    return render(request, 'user_response.html', {
        'responses': response})


@login_required  # проверка зареган ли user
def accept_response(request, pk):
    r = Response.objects.filter(id=pk)
    response = Response.objects.get(id=pk)
    p = response.commentPost.id
    print(response.status)
    if response.status:
        r.update(status=False)
    else:
        r.update(status=True)
    return redirect(reverse('user_response', args=[str(p)]))
