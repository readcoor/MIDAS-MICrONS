"""microns project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from microns.settings import API_VERSION
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView, TemplateView
from .views import schema_view, index, health_check

redirect_homepage_view = RedirectView.as_view(url='https://wyssmicrons.github.io/MIDAS-MICrONS/', permanent=True)
favicon_view  = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    url(r'^$', index),
    url(r'^favicon\.ico$', favicon_view),
    url(r'^admin', admin.site.urls),
    url(r'^health', health_check),
    url(r'^docs', schema_view),
    url(r'openid', include('djangooidc.urls')),
    url('^', include('nada.urls'))
    ]

