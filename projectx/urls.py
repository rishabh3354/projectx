"""projectx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.generic import RedirectView

from apps.accounts import views


urlpatterns = [
    path('admin/', admin.site.urls),

    # login
    url(r'^login/', views.login_user, name="login"),
    url(r'^login-request/', views.login_request, name="login-request"),
    url(r'^logout/', views.logout_user, name="logout"),
    url(r'^signup/', views.get_signup_page, name='signup'),
    url(r'^signup-user/', views.signup_user, name='signup-user'),

    # home
    url(r'^$', views.home, name='home'),
    # social-auth
    path('accounts/', include('allauth.urls')),
    # contact us
    path("contact_us/", views.contact_create, name="contact_us"),
    path(r'account/', include("apps.accounts.urls")),

    # set your password
    url(r'^set_password/', views.set_your_password, name='set_password'),
    url(r'^set_password_success/', views.set_your_password_success, name='set_password_success'),
    url(r'^set_password_fail/', views.set_your_password_failed, name='set_password_fail'),
    url(r'^change_password/', views.change_password, name='change_password'),
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")), ),

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'apps.accounts.views.handler404'
handler500 = 'apps.accounts.views.handler500'
