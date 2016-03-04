# -*- coding: utf-8 -*-
from django.contrib import admin

from blog.models import *
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):

    list_display = ('title','desc','is_recommend',)
    list_display_links = ('title',)
    list_editable = ('is_recommend',)

    fieldsets = (
        (None, {
            'fields': ('title', 'desc','content')
        }),
        ('高级', {
            'classes': ('collapse',),
            'fields': ('click_count','is_recommend','user','category','tag')
        }),
    )

    class Media:
        js= (
            '/static/js/kindeditor-4.1.10/kindeditor-min.js',
            '/static/js/kindeditor-4.1.10/lang/zh_CN.js',
            '/static/js/kindeditor-4.1.10/config.js',


        )


admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Ad)
admin.site.register(Catagory)
admin.site.register(Links)
admin.site.register(Comment)



