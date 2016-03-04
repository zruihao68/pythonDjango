# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(blank=True, verbose_name='last login', null=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], unique=True, error_messages={'unique': 'A user with that username already exists.'}, verbose_name='username', max_length=30)),
                ('first_name', models.CharField(blank=True, verbose_name='first name', max_length=30)),
                ('last_name', models.CharField(blank=True, verbose_name='last name', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='email address', max_length=254)),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', verbose_name='staff status', default=False)),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active', default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatar/%Y/%m', default='avatar/default.png', verbose_name='用户头像', max_length=200)),
                ('qq', models.CharField(max_length=20, blank=True, verbose_name='QQ号码', null=True)),
                ('mobile', models.CharField(max_length=11, unique=True, blank=True, verbose_name='手机号码', null=True)),
                ('url', models.URLField(max_length=100, blank=True, verbose_name='个人网页地址', null=True)),
                ('groups', models.ManyToManyField(related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', blank=True, to='auth.Group', related_name='user_set', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', help_text='Specific permissions for this user.', blank=True, to='auth.Permission', related_name='user_set', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(verbose_name='广告标题', max_length=50)),
                ('description', models.CharField(verbose_name='广告描述', max_length=200)),
                ('image_url', models.ImageField(upload_to='ad/%Y/%m', verbose_name='图片路径')),
                ('callback_url', models.URLField(blank=True, verbose_name='回调url', null=True)),
                ('date_publish', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('index', models.IntegerField(default=999, verbose_name='排列顺序(从小到大)')),
            ],
            options={
                'ordering': ['index', 'id'],
                'verbose_name': '广告',
                'verbose_name_plural': '广告',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(verbose_name='文章标题', max_length=50)),
                ('desc', models.CharField(verbose_name='文章描述', max_length=50)),
                ('content', models.TextField(verbose_name='文章内容')),
                ('click_count', models.IntegerField(default=0, verbose_name='点击次数')),
                ('is_recommend', models.BooleanField(verbose_name='是否推荐', default=False)),
                ('date_publish', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
            ],
            options={
                'ordering': ['-date_publish'],
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
            },
        ),
        migrations.CreateModel(
            name='Catagory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='分类名称', max_length=20)),
                ('index', models.IntegerField(default=999, verbose_name='分类排序')),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('content', models.TextField(verbose_name='评论内容')),
                ('username', models.CharField(max_length=30, blank=True, verbose_name='用户名', null=True)),
                ('email', models.EmailField(max_length=50, blank=True, verbose_name='邮箱地址', null=True)),
                ('url', models.URLField(max_length=100, blank=True, verbose_name='个人网页地址', null=True)),
                ('date_publish', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('article', models.ForeignKey(blank=True, null=True, to='blog.Article', verbose_name='文章')),
                ('pid', models.ForeignKey(blank=True, null=True, to='blog.Comment', verbose_name='父级评论')),
                ('user', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
            },
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(verbose_name='标题', max_length=50)),
                ('description', models.CharField(verbose_name='友情链接描述', max_length=200)),
                ('callback_url', models.URLField(verbose_name='url地址')),
                ('date_publish', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('index', models.IntegerField(default=999, verbose_name='排列顺序(从小到大)')),
            ],
            options={
                'ordering': ['index', 'id'],
                'verbose_name': '友情链接',
                'verbose_name_plural': '友情链接',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='标签名称', max_length=30)),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(blank=True, null=True, to='blog.Catagory', verbose_name='分类'),
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(to='blog.Tag', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
    ]
