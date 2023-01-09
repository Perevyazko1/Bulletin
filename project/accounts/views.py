from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic.edit import CreateView

from bulletin.models import AuthUser
from .forms import SignUpForm, AuthenticateForm


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login'

    template_name = 'registration/signup.html'


def authenticate(request):
    code = AuthUser.objects.get(user=request.user)
    form = AuthenticateForm(request.POST or None)
    if request.method == 'POST':
        data = request.POST.get('code')
        if str(code.uuid) == data:
            a = AuthUser.objects.filter(user=request.user)
            a.update(authenticate=True)
    return render(request, 'registration/insert_code.html', {
        'form': form,
        'authenticate': code.authenticate

    })
