# coding: utf-8
"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import patterns,include,url
from django.contrib import admin
from article import views as article_views

from article.views import RSSFeed
urlpatterns = [
	# Examples:
	# url(r'^$','my_blog.views.home',name='home'),
	# url(r'^blog/', include('blog.urls')),
        url(r'^admin/', include(admin.site.urls)), #可以使用设置好的url进入网站后台
        url(r'^$', 'article.views.home', name = 'home'),
        url(r'^(?P<id>\d+)/$', 'article.views.detail', name='detail'),
        url(r'^aboutme/$', 'article.views.about_me', name='about_me'),    
        url(r'^tag(?P<tag>\w+)/$','article.views.search_tag', name='search_tag'),
        url(r'^archives/$','article.views.archives', name='archives'),
        url(r'^search/$','article.views.blog_search', name = 'search'),
        url(r'^feed/$', RSSFeed(), name = "RSS"),  #新添加的urlconf, 并将name设置为RSS, 方便在模板中使用url
        url(r'^online/', include('article.urls')),
    ]
