"""bolg_project URL Configuration

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
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from blog.views import index, archive, article,do_login, comment_post, do_reg, do_logout, catagory_archive

urlpatterns = [
    url(r'^$',index,name='index'),
    url(r'^archive$',archive,name='archive'),
    url(r'^catagory$',catagory_archive,name='catagory'),
    url(r'^article$',article,name='article'),
    url(r'^login',do_login,name='login'),
    url(r'^do_reg',do_reg,name='reg'),
    url(r'^logout',do_logout,name='logout'),
    url(r'^comment_post$',comment_post,name='comment_post'),
]
