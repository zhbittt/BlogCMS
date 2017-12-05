from django import forms
from django.forms import widgets,ValidationError
from blog.models import *

from blog.plugins import xss_plugin
class LoginForm(forms.Form):
    username = forms.CharField(label='username',max_length=100)
    password = forms.CharField(label='password',max_length=100)

    def clean_username(self):
        if len(self.cleaned_data.get('username'))>5:
            print(self.cleaned_data.get('password'))
            return self.cleaned_data.get('username')
        else:
            raise ValidationError("用户名长度小于5")
    def clean_password(self):
        pass

    def clean(self):
        if  self.cleaned_data["password"] == self.cleaned_data['repeat_password']:
            return  self.cleaned_data


class RegForm(forms.Form):

    username = forms.CharField(
        max_length=12,min_length=5,
        error_messages={"required":"用户名不能为空"},
        widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"username"}))

    password = forms.CharField(
        min_length=5,
        widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"password"}))

    repeat_pwd = forms.CharField(
        min_length=5,
        widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"repeat_pwd"}))

    email = forms.EmailField(
        widget=widgets.EmailInput(attrs={"class":"form-control","placeholder":"email"}))

    def clean_username(self):

        ret = UserInfo.objects.filter(username=self.cleaned_data.get("username"))

        if not ret:
            return self.cleaned_data.get("username")
        else :
            raise  ValidationError("用户名已注册")

    def clean_password(self):

        data =self.cleaned_data.get("password")

        if not data.isdigit():
            return self.cleaned_data.get("password")
        else:
            raise ValidationError("密码不能全为数字")

    def clean_validCode(self):
        if self.cleaned_data.get("validCode") == self.request.session.get("validCode"):
            return self.cleaned_data.get("validCode")
        else:
            raise ValidationError("验证码错误")


    def clean(self):
        if self.cleaned_data.get("password") == self.cleaned_data.get("repeat_pwd"):
            return self.cleaned_data
        else:
            raise  ValidationError("两次密码不一致")

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request=request


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=20,error_messages={"required":"不能为空"},
            widget=widgets.TextInput(attrs={"class":"form-control"}))
    content = forms.CharField(error_messages={"required":"不能为空"},
            widget=widgets.Textarea(attrs={"class":"form-control"}))

    category_id = forms.ChoiceField(choices=[])

    tag_id = forms.MultipleChoiceField(choices=[])
    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        user_obj=request.user.nid
        print("user_obj---------",user_obj)
        self.fields['category_id'].choices=Category.objects.filter(blog__user_id=user_obj).values_list("nid","title")
        self.fields['tag_id'].choices=Article2Tag.objects.filter(article__user_id=user_obj).values_list("tag__nid","tag__title")


    def clean_content(self):
        html_str = self.cleaned_data.get("content")
        clean_content = xss_plugin.filter_xss(html_str)
        self.cleaned_data["content"]= clean_content
        return self.cleaned_data.get("content")