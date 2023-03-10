"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from accounts.views import authenticate
from bulletin.views import send_mail, successful_submission
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_send_mail/', send_mail, name='sendmail'),
    path('successful_submission/', successful_submission, name='successful_submission'),
    path('bulletin/', include('bulletin.urls')),
    path(r'ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/", include("accounts.urls")),
    path("authenticate/", authenticate, name='authenticate'),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
