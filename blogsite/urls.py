"""
URL configuration for blogsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path
from django.views.generic.base import TemplateView 
from django.contrib.sitemaps.views import sitemap
from jsl_django_sitemap.views import sitemaps
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('contentfeed.urls')),
    # Extras 
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),),
    path("site.webmanifest",TemplateView.as_view(template_name="site.webmanifest", content_type="text/plain"),),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico'))),
    path('favicon-16x16.png', RedirectView.as_view(url=staticfiles_storage.url('images/favicon-16x16.png'))),
    path('favicon-32x32.png', RedirectView.as_view(url=staticfiles_storage.url('images/favicon-32x32.png'))),
    path('apple-touch-icon.png', RedirectView.as_view(url=staticfiles_storage.url('images/apple-touch-icon.png'))),
]
