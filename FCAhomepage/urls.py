"""FCAhomepage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

# 以上为django初始页面


from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

from . import views,testdb,register,login,modify

urlpatterns = [
    url(r'^$', views.index),
    url(r'hello/', views.hello),
    #url(r'register/', views.register),
    url(r'^login/$', views.login),
    url(r'^\d+\.\d+$', views.pages),
    url(r'^[\S]+\.html$', views.byUrl),
    path('database/', include('database.urls')),
    path('testdb/', testdb.testdb),
    path('admin/', admin.site.urls),
    url(r'^register_form/$', register.register_form),
    url(r'^register/$', register.register),
    url(r'^login_action/$', login.login_action),
    url(r'^logout/$', views.logout),
    url(r'^modify/$', modify.modify),
    url(r'^modify_action/$', modify.modify_action),
    url(r'^record/$', views.record),
    url(r'^tutorial/$', views.tutorial),

]