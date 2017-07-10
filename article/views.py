#coding:utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from article.models import Article
from datetime import datetime
from django.http import Http404
from django.contrib.syndication.views import Feed  #注意加入import语句
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms
from models import User
from django.template import RequestContext

# Create your views here.
def home(request):
	posts = Article.objects.all() #获取全部的Article对象
	paginator = Paginator(posts, 2)
	page = request.GET.get('page')
	try :
		post_list = paginator.page(page)
	except PageNotAnInteger :
		post_list = paginator.page(1)
	except EmptyPage :
		post_list = paginator.paginator(paginator.num_pages)
	return render(request, 'home.html', {'post_list' : post_list})

def detail(request, id):
	try:
		post = Article.objects.get(id=str(id))
	except Article.DoesNotExist:
		raise Http404
	return render(request, 'post.html', {'post' : post})

def about_me(request) :
	return render(request, 'aboutme.html')

def search_tag(request, tag) :
	try:
		post_list = Article.objects.filter(category__iexact = tag) #contains
	except Article.DoesNotExist :
		raise Http404
	return render(request, 'tag.html', {'post_list' : post_list})

def archives(request) :
	try:
		post_list = Article.objects.all()
	except Article.DoesNotExist :
		raise Http404
	return render(request, 'archives.html', {'post_list' : post_list,'error' : False})		

def blog_search(request):
    if 's' in request.GET:
        s = request.GET['s']
        if not s:
            return render(request,'home.html')
        else:
            post_list = Article.objects.filter(title__icontains = s)
            if len(post_list) == 0 :
                return render(request,'archives.html', {'post_list' : post_list,
                                                    'error' : True})
            else :
                return render(request,'archives.html', {'post_list' : post_list,
                                                    'error' : False})
    return redirect('/')

class RSSFeed(Feed) :
    title = "RSS feed - article"
    link = "feeds/posts/"
    description = "RSS feed - blog posts"

    def items(self):
        return Article.objects.order_by('-date_time')

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.date_time

    def item_description(self, item):
        return item.content

class UserForm(forms.Form):
	username = forms.CharField(label='用户名',max_length=100)
	password = forms.CharField(label='密码',widget=forms.PasswordInput())

#注册
def regist(req):
	if req.method == 'POST':
		uf = UserForm(req.POST)
		if uf.is_valid():
			#获得表单数据
			username = uf.cleaned_data['username']
			password = uf.cleaned_data['password']
			#添加到数据库
			User.objects.create(username= username,password=password)
			return HttpResponse('regist success!!')
	else:
		uf = UserForm()
	return render_to_response('regist.html',{'uf':uf},context_instance=RequestContext(req))

	#登录
def login(req):
	if req.method == 'POST':
		uf = UserForm(req.POST)
		if uf.is_valid():
			#获取表单用户密码
			username = uf.cleaned_data['username']
			password = uf.cleaned_data['password']
			#获取的表单数据与数据库进行比较
			user = User.objects.filter(username__exact = username,password__exact = password)
			if user:
				#比较成功，跳转index
				response = HttpResponseRedirect('/online/index/')
				#将username写入浏览器cookie，失效时间为3600
				response.set_cookie('username',username,3600)
				return response
			else:
				#比较失败，还在login
				return HttpResponseRedirect('/online/login/')
	else:
		uf = UserForm()
	return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(req))

#登陆成功
def index(req):
	username = req.COOKIES.get('username','')
	return render_to_response('index.html' ,{'username':username})

#退出
def logout(req):
	response = HttpResponse('logout !!')
	#清理cookie里保存username
	response.delete_cookie('username')
	return response
