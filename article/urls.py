from django.conf.urls import patterns, url



urlpatterns = [
    # Examples:
    # url(r'^$', 'mysite5.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

  	url(r'^$', 'article.views.login', name='login'),
  	url(r'^login/$','article.views.login',name = 'login'),
  	url(r'^regist/$','article.views.regist',name = 'regist'),
  	url(r'^index/$','article.views.index',name = 'index'),
  	url(r'^logout/$','article.views.logout',name = 'logout'),
]
