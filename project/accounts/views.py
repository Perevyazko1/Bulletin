from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic.edit import CreateView

from bulletin.models import AuthUser
from .forms import SignUpForm, AuthenticateForm


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login'

    template_name = 'registration/signup.html'
    # success_url = reverse_lazy('authenticate')



# class Authenticate(View):
#     # model = AuthUser
#     form_class = AuthenticateForm
#     success_url = '/authenticate'
#
#     template_name = 'registration/insert_code.html'


def authenticate(request):
    code = AuthUser.objects.get(user=request.user)
    form = AuthenticateForm(request.POST or None)
    print(code.uuid)
    if request.method =='POST':
        data = request.POST.get('code')
        if str(code.uuid) == data:
            a=AuthUser.objects.filter(user=request.user)
            a.update(authenticate=True)
    # if form.is_valid():
    #     data = form.cleaned_data.get("code")
    #     print(data)
    return render(request, 'registration/insert_code.html', {
        'form': form,
        'authenticate': code.authenticate

    })
