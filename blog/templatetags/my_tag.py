from django import template
from django.utils.safestring import mark_safe
from blog.models import *
register = template.Library()  # register的名字是固定的,不可改变

import datetime
# @register.filter
# def filter_multi(v1, v2):
#     return v1 * v2
#
# @register.simple_tag
# def simple_tag_multi(v1,v2):
#     return  v1 * v2
@register.filter
def siteArticle(siteArticle_obj,site_nid):
    return siteArticle_obj.objects.filter(siteCategory=site_nid).values_list("nid","name")


@register.filter
def yuanling(t):



    user_create_time=datetime.datetime(year=t.year,month=t.month,day=t.day,hour=t.hour,minute=t.minute,second=t.second)
    ret=datetime.datetime.now()-user_create_time

    print(ret)
    print(type(ret))

    return mark_safe(ret)
