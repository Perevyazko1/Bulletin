from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import PostForm, ResponseForm, SendMailForm
from .models import AuthUser, Post, Response, User
from .tasks import submission_news


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
        context['authenticate'] = AuthUser.objects.get(user=self.request.user)
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_id.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authenticate'] = AuthUser.objects.get(user=self.request.user)
        return context


class PostList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'post.html'
    context_object_name = 'post'
    paginate_by = 10


class PostCreate(LoginRequiredMixin, CreateView):
    permission_required = ('bulletin.add_news',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'edit_post.html'

    def form_valid(self, form):

        self.object = form.save(commit=False
                                )
        self.object.author = User.objects.get(id=self.request.user.id)
        return super().form_valid(
            form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    permission_required = ('bulletin.change_news',)
    form_class = PostForm
    model = Post
    template_name = 'edit_post.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    permission_required = ('bulletin.delete_news',)
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('post_list')


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


@login_required
def user_response(request, pk):
    post = Post.objects.get(id=pk)
    response = Response.objects.filter(commentPost=post)
    return render(request, 'user_response.html', {
        'responses': response})


@login_required
def accept_response(request, pk):
    r = Response.objects.filter(id=pk)
    response = Response.objects.get(id=pk)
    p = response.commentPost.id
    if response.status:
        r.update(status=False)
    else:
        response.save()
        r.update(status=True)
    return redirect(reverse('user_response', args=[str(p)]))


@login_required
def delete_response(request, pk):
    response = Response.objects.get(id=pk)
    p = response.commentPost.id
    response.delete()
    return redirect(reverse('user_response', args=[str(p)]))


@user_passes_test(lambda u: u.is_superuser)
def send_mail(request):
    form = SendMailForm(request.POST or None)
    if request.method == 'POST':
        data = request.POST.get('text')
        users = User.objects.all()
        emails = []
        if form.is_valid():
            for user in users:
                emails += [user.email]
            submission_news.delay(data, emails)

            return redirect(reverse('successful_submission'))
    return render(request, 'send_mail.html', {
        'form': form
    })


@user_passes_test(lambda u: u.is_superuser)
def successful_submission(request):
    return render(request, 'successful_submission.html')