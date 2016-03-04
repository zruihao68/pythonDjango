import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings

from blog.forms import CommentForm, LoginForm, RegForm
from blog.models import Article, Ad, Tag
from blog.models import Catagory, Comment, User
from django.db.models import Count
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger

logger = logging.getLogger("blog.views")


def global_setting(request):
    # 站点基本信息
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC

    # 分类信息
    catagory_list = Catagory.objects.all()[:6]

    # 广告信息
    ad_List = Ad.objects.all()[:4]

    # 归档信息
    archive_list = Article.objects.distinct_date()

    # 标签云
    tag_list = Tag.objects.all()

    # 评论排行
    comment_count_list = Comment.objects.values("article").annotate(comment_count=Count('article')).order_by(
        '-comment_count')
    article_comment_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list]

    # 浏览排行
    article_click_list = Article.objects.all().order_by('-click_count')

    # 站长推荐
    article_is_recommend_list = Article.objects.filter(is_recommend=True).order_by('-date_publish')

    return locals()


# Create your views here.
def index(request):
    try:
        # 文章内容
        article_list = Article.objects.all()

        article_list = getPage(request, article_list, 2)
    except Exception as e:
        logger.error(e)
    # return render(request, 'index.html', {'article_list':article_list,'catagory_list':catagory_list,'ad_list':ad_List})
    return render(request, 'index.html', locals())


# 分页
def getPage(request, pageItems, pageSize):
    # 分页 每页显示10条
    paginator = Paginator(pageItems, pageSize)
    try:
        page = int(request.GET.get('page', 1))
        pageItems = paginator.page(page)
    except (InvalidPage, EmptyPage, PageNotAnInteger):
        pageItems = paginator.page(1)

    return pageItems


def archive(request):
    try:
        year = request.GET.get("year", None)
        month = request.GET.get("month", None)
        # 文章内容
        article_list = Article.objects.filter(date_publish__icontains=year + '-' + month)
        # 分页
        article_list = getPage(request, article_list, 2)
    except Exception as e:
        logging.error(e)

    return render(request, 'archive.html', locals())


def article(request):
    try:
        try:
            id = request.GET.get("id", None)
            article = Article.objects.get(pk=id)
        except (Article.DoesNotExist):
            return render(request, "failure.html", {"reason": "没有该文章"})
        # 评论表单
        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'url': request.user.url,
                                    'article': id} if request.user.is_authenticated() else{'article': id})

        # 获取评论信息
        comments = Comment.objects.filter(article=article).order_by("id")
        comment_list = []
        for comment in comments:
            for item in comment_list:
                if not hasattr(item, "children_comment"):
                    setattr(item, 'children_comment', [])  # setattr(x,“foobar”,123)相当于x.foobar = 123。
                if comment.pid == item:
                    item.children_comment.append(comment)
                    break;
            if comment.pid is None:
                comment_list.append(comment)
    except Exception as e:
        logging.error(e)
    return render(request, "article.html", locals())


# 评论提交
def comment_post(request):
    try:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():  # 如果表单提交的数据合法
                comment = Comment.objects.create(username=form.cleaned_data['author'],
                                                 email=form.cleaned_data["email"],
                                                 url=form.cleaned_data["url"],
                                                 content=form.cleaned_data["comment"],
                                                 article_id=form.cleaned_data["article"],
                                                 user=request.user if request.user.is_authenticated() else None)
                comment.save()
            else:
                return render(request, 'failure.html', {'reason': form.errors})
    except Exception as  e:
        logging.error("评论提交", e)
    return redirect(request.META['HTTP_REFERER'])

# 登录
def do_login(request):
    try:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                # 登录
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'reason': '登录验证失败'})
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': form.errors})
        else:
            loginForm = LoginForm()
    except Exception as e:
        logging.error("登录异常", e)
    return render(request, 'login.html', locals())


def do_reg(request):
    '''
    注册
    :param request:
    :return:
    '''
    try:
        if request.method == "POST":
            form = RegForm(request.POST)
            if form.is_valid():
                  # 注册
                user = User.objects.create(username=form.cleaned_data["username"],
                                    email=form.cleaned_data["email"],
                                    url=form.cleaned_data["url"],
                                    password=make_password(form.cleaned_data["password"]),)
                user.save()

                # 登录
                user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                login(request, user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': form.errors})

        else:
            form = RegForm()
    except Exception as e:
        logging.error("注册", e)
    return render(request, "reg.html", locals())


# 注销
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        logger.error("注销",e)
    return redirect(request.META['HTTP_REFERER'])


def catagory_archive(request):
    '''
    分类文章
    :param request:
    :return:
    '''
    try:
        catagory = request.GET.get("id", None)
        # 文章内容
        article_list = Article.objects.filter(category = catagory)
        # 分页
        article_list = getPage(request, article_list, 2)
    except Exception as e:
        logging.error(e)

    return render(request, 'archive.html', locals())


