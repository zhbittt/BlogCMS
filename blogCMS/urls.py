"""blogCMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin
from blog import views

from blog.views import pcgetcaptcha
from blog.views import pcajax_validate


from django.views.static import serve
from blogCMS import  settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.index),



    url(r'^home/', views.home),


    url(r'^login/', views.login),
    url(r'^get_validCode_img/', views.get_validCode_img),
    url(r'^reg/', views.reg),
    url(r'^index',views.index),
    url(r'^logout', views.logout),
    url(r'^cate/(?P<site_article_category>.*)/$',views.index),

    url(r'^blog/', include('blog.urls')),
    url(r'^turn/', views.turn),


    #滑动验证码
    url(r'^pc-geetest/register', pcgetcaptcha, name='pcgetcaptcha'),
    url(r'^pc-geetest/ajax_validate', pcajax_validate, name='pcajax_validate'),

    # media 配置
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    #上传的图片
    url(r'^uploadFile/', views.uploadFile),



]
