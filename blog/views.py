from django.shortcuts import render,redirect,HttpResponse

# Create your views here.
from  django.contrib import auth
from blog import forms
from blog.models import *
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO
from django.db.models import Count,F
from django.db import transaction
from blogCMS import settings
import random
import json,os
from django.http import JsonResponse
import datetime


from blog.geetest import GeetestLib

pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"
mobile_geetest_id = "7c25da6fe21944cfe507d2f9876775a9"
mobile_geetest_key = "f5883f4ee3bd4fa8caec67941de1b903"

#
def pcgetcaptcha(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)

# def pcajax_validate(request):
#     if request.method == "POST":
#         gt = GeetestLib(pc_geetest_id, pc_geetest_key)
#         challenge = request.POST.get(gt.FN_CHALLENGE, '')
#         validate = request.POST.get(gt.FN_VALIDATE, '')
#         seccode = request.POST.get(gt.FN_SECCODE, '')
#         status = request.session[gt.GT_STATUS_SESSION_KEY]
#         user_id = request.session["user_id"]
#         if status:
#             result = gt.success_validate(challenge, validate, seccode, user_id)
#         else:
#             result = gt.failback_validate(challenge, validate, seccode)
#         result = {"status":"success"} if result else {"status":"fail"}
#         return HttpResponse(json.dumps(result))
#     return HttpResponse("error")
def pcajax_validate(request):
    if request.method == "POST":

        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {"status":"success"} if result else {"status":"fail"}
        return HttpResponse(json.dumps(result))
    return HttpResponse("error")



#图片   滑动  点击登录   login 添加版
def login(request):
    print("login------------------------------------------------",request.session.get("refer"))
    print(request.session.items())
    print(request.POST)
    if request.is_ajax():

        username = request.POST.get("username")
        password = request.POST.get("password")
        validCode = request.POST.get("validCode")

        login_response = {"is_login":False,"error_msg":None}
        if validCode.upper() == request.session.get("keepValidCode").upper():
            user = auth.authenticate(username=username,password=password)
            if user:
                login_response["is_login"]=True
                auth.login(request,user)
            else:
                login_response["error_msg"]='账号或密码错误'
        else:
            login_response["error_msg"] = '验证码错误'

        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)

        login_response["status"]=True if result else False

        return JsonResponse(login_response)
    return render(request,'login.html')

#图片点击   登录  login 原始版本
# def login(request):
#     print("login------------------------------------------------", request.session.get("refer"))
#     if request.is_ajax():
#
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         validCode = request.POST.get("validCode")
#
#         login_response = {"is_login": False, "error_msg": None}
#         if validCode.upper() == request.session.get("keepValidCode").upper():
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 login_response["is_login"] = True
#                 auth.login(request, user)
#             else:
#                 login_response["error_msg"] = '账号或密码错误'
#         else:
#             login_response["error_msg"] = '验证码错误'
#         return HttpResponse(json.dumps(login_response))
#     return render(request, 'login.html')
#



def home(request):
    return render(request,'home.html')

def get_validCode_img(request):
    '''
    获取验证码图片
    '''
    img = Image.new(mode="RGB" , size=(120,40) ,color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))

    draw = ImageDraw.Draw(img,"RGB")
    font = ImageFont.truetype('blog/static/font/kumo.ttf',25)

    valid_list=[]
    for i in range(5):

        random_num =str(random.randint(0,9))
        random_lower_zimu =chr(random.randint(65,90))
        random_upper_zimu = chr(random.randint(97,122))

        random_char = random.choice([random_num,random_lower_zimu,random_upper_zimu])
        draw.text([5+i*24,10],random_char,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),font=font)
        valid_list.append(random_char)

    f = BytesIO()
    img.save(f,'png')
    data = f.getvalue()

    valid_str = "".join(valid_list)
    print(valid_str)

    request.session["keepValidCode"]=valid_str

    return HttpResponse(data)

def reg(request):
    if request.is_ajax():
        form_obj = forms.RegForm(request,request.POST)

        regResponse = {"user":None,"errorList":None}

        if form_obj.is_valid():
            username = form_obj.cleaned_data.get("username")
            password = form_obj.cleaned_data.get("password")
            email = form_obj.cleaned_data.get("email")
            avatar_img = request.FILES.get("avatar_img")

            user_obj = UserInfo.objects.create_user(username=username,password=password,email=email,avatar=avatar_img,nickname=username)

            regResponse["user"]=user_obj.username

        else:
            regResponse["errorList"]=form_obj.errors

        return HttpResponse(json.dumps(regResponse))


    form_obj = forms.RegForm(request)
    return render(request,"reg.html",{"form_obj":form_obj})

def index(request,*args,**kwargs):
    print("index------------------------",request.body)
    if kwargs:
        article = Article.objects.filter(category__title=kwargs.get("site_article_category"))
    else:
        article = Article.objects.all()
    siteCategory = SiteCategory.objects.all()
    # siteArticlecategory=SiteArticlecategory.objects.all()

    content={"siteCategory":siteCategory,"article":article}
    request.session["referror"] = request.path
    return render(request,'index.html',content)

def logout(request):
    auth.logout(request)

    return redirect("/login/")

def homeSite(request,username,**kwargs):
    print('---------------',kwargs)
    print("homeSite")
    print(request.path)
    print(request.session.items())
    user_obj = UserInfo.objects.filter(nickname=username).first()
    if not user_obj:
        return render(request,'no_found.html')
    user_blog = user_obj.blog.nid
    #文章内容
    print(kwargs)
    if kwargs:
        if kwargs.get("condition") == 'category':
            article_list = Article.objects.filter(user=user_obj,category__title=kwargs.get("para"))
        elif kwargs.get("condition") == 'tag':
            article_list = Article.objects.filter(user=user_obj,tag__title=kwargs.get("para"))
        elif kwargs.get("condition") == 'archive':
            year,month=kwargs.get("para").split("/")
            print(year,month)
            article_list = Article.objects.filter(user=user_obj, create_time__year=year,create_time__month=month)
        elif kwargs.get("condition") == 'articles':
            article_list = ArticleDetail.objects.filter(article__nid=kwargs.get("para"))
    else:
        article_list = Article.objects.filter(user=user_obj)

    #分类归档
    category_list=Category.objects.filter(blog=user_blog).annotate(c=Count("article__nid")).values_list("title","c")

    #标签归档
    tag_list=Tag.objects.filter(blog=user_blog).annotate(c=Count("article__nid")).values_list("title","c")

    #时间归档
    data_list=Article.objects.filter(user=user_obj).extra(select={"time":"strftime('%%Y/%%m',create_time)"}).values_list("time").annotate(Count("nid"))

    content={"user_obj":user_obj,"article_list":article_list,"category_list":category_list,"tag_list":tag_list,"data_list":data_list}
    obj=render(request, 'homeSite.html', content)
    obj.set_cookie("luo", "luo1")
    return obj

def articleDetail(request,username,article_id):

    user_obj = UserInfo.objects.filter(username=username).first()
    if not user_obj:
        return render(request, 'no_found.html')
    user_blog = user_obj.blog.nid

    # 文章内容
    articledetail = ArticleDetail.objects.filter(article=article_id).first()
    # 分类归档
    category_list = Category.objects.filter(blog=user_blog).annotate(c=Count("article__nid")).values_list("title", "c")

    # 标签归档
    tag_list = Tag.objects.filter(blog=user_blog).annotate(c=Count("article__nid")).values_list("title", "c")

    # 时间归档
    data_list = Article.objects.filter(user=user_obj).extra(
        select={"time": "strftime('%%Y/%%m',create_time)"}).values_list("time").annotate(Count("nid"))

    comment_list = Comment.objects.filter(article=article_id)
    content = {"user_obj": user_obj, "articledetail": articledetail, "category_list": category_list, "tag_list": tag_list,
               "data_list": data_list,"comment_list":comment_list}
    return render(request, 'article_content.html', content)

def poll(request):
    '''
    点赞
    '''
    user_id = request.POST.get("user_id")
    article_id = request.POST.get("article_id")
    poll_response = {"is_login": False, "is_repeat": False}
    print(user_id,article_id)
    if not user_id:

        return HttpResponse(json.dumps(poll_response))

    poll_response["is_login"] = True

    if ArticleUp.objects.filter(user_id=user_id,article_id=article_id):
        poll_response["is_repeat"]=True
    else:
        with transaction.atomic():
            Up_obj=ArticleUp.objects.create(user_id=user_id,article_id=article_id)
            if request.POST.get("vote")=="diggit":
                Article.objects.filter(nid=article_id).update(up_count=F("up_count") + 1)
            else:
                Article.objects.filter(nid=article_id).update(down_count=F("down_count") + 1)

    return HttpResponse(json.dumps(poll_response))

def comment(request):
    '''
    评论
    '''
    article_id = request.POST.get("article_id")

    comment_content = request.POST.get("comment_content")
    user_id = request.POST.get("user_id")

    commentResponse = {"is_login":False}
    print("user_id",user_id)
    print("comment_content",comment_content)
    print("article_id",article_id)
    if not user_id:
        return JsonResponse(commentResponse)

    commentResponse["is_login"]=True
    print(request.POST.get("parent_comment_id"), "=======")
    if request.POST.get("parent_comment_id"):    #   处理子评论
        with transaction.atomic():
            pid=request.POST.get("parent_comment_id")
            comment_obj=Comment.objects.create(article_id=article_id,user_id=user_id,content=comment_content,parent_comment_id=pid)
            commentResponse["parent_comment_username"] = comment_obj.parent_comment.user.username
            commentResponse["parent_comment_content"] = comment_obj.parent_comment.content

    else:   #  处理的文章评论，即根评论
        with transaction.atomic():
            comment_obj=Comment.objects.create(article_id=article_id,user_id=user_id,content=comment_content)
            Article.objects.filter(nid=article_id).update(comment_count=F("comment_count")+1)


    commentResponse["comment_data"] = str(comment_obj.comment_data)
    commentResponse["comment_id"] = comment_obj.nid
    return JsonResponse(commentResponse)

def commentTree(request,article_id):

    comment_list=Comment.objects.filter(article_id=article_id).extra(select={"comment_data":"strftime('%%Y-%%m-%%d  %%H-%%M',comment_data)"}).values("nid","content","parent_comment_id","user__username","user__avatar","comment_data")
    print(comment_list)
    comment_dict={}
    for comment in comment_list:
        comment["children_commentList"]=[]
        comment_dict[comment["nid"]]=comment

    #=====找父级评论
    commentTree=[]

    for comment in comment_list:
        pid = comment.get("parent_comment_id")
        if pid:
            comment_dict[pid]["children_commentList"].append(comment)
        else:
            commentTree.append(comment)
    return HttpResponse(json.dumps(commentTree))


def backendIndex(request):
    print(request.user.is_authenticated())
    if not request.user.is_authenticated():
        return redirect('/login/')

    article_list=Article.objects.filter(user_id=request.user.nid)
    context={"article_list":article_list}
    return render(request,"backendIndex.html",context)


def addArticle(request):
    print("addArticle------------------------", request.body)
    addResponse = {"is_login":False,"errorList":None}
    if not request.user.is_authenticated():
        return HttpResponse(json.dumps(addResponse))
    if request.is_ajax():
        article_form = forms.ArticleForm(request,data=request.POST)
        addResponse["is_login"]=True
        if article_form.is_valid():
            title = article_form.cleaned_data.get("title")
            content = article_form.cleaned_data.get("content")
            article_obj=Article.objects.create(title=title,desc=content[0:50],create_time=datetime.datetime.now(),user_id=request.user.nid)
            ArticleDetail.objects.create(content=content,article=article_obj)
        else:
            addResponse["errorList"]=article_form.errors
        return JsonResponse(addResponse)
    # if  request.method=="POST":
    #     article_form = forms.ArticleForm(request.POST)
    #     if article_form.is_valid():
    #         title = article_form.cleaned_data.get("title")
    #         content = article_form.cleaned_data.get("content")
    #         article_obj=Article.objects.create(title=title,desc=content[0:50],comment_data=datetime.datetime.now())
    #         ArticleDetail.objects.create(content=content,user=article_obj)
    #         return render(request, 'success.html', {"info": "添加文章"})
    #     return render(request, 'addArticle.html', {"article_form": article_form})

    article_form = forms.ArticleForm(request)

    return render(request,'addArticle.html',{"article_form":article_form})


def uploadFile(request):
    print("POST",request.POST)
    print("FILES",request.FILES)


    file_obj = request.FILES.get("imgFile")
    file_name = file_obj.name
    path = os.path.join(settings.MEDIA_ROOT,'article_uploads',file_name)
    with open(path,"wb") as f:
        for i in file_obj:
            f.write(i)

    response={
        "error":0,
        "url":"/media/article_uploads/"+file_name+"/"
    }
    return HttpResponse(json.dumps(response))


def turn(request):
    return redirect('/index/')




