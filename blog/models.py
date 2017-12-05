from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserInfo(AbstractUser):
    '''
    用户信息
    '''
    nid = models.BigAutoField(primary_key=True)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    telephone = models.CharField(verbose_name='手机号码', max_length=11, blank=True, null=True, unique=True)
    avatar = models.FileField(verbose_name='头像', upload_to='avatar', default="/media/avatar/default.png")
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.username


class Blog(models.Model):
    '''
    站点信息
    '''
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    site = models.CharField(verbose_name='个人博客后缀', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题', max_length=32)

    user = models.OneToOneField(to='UserInfo', to_field='nid')

    def __str__(self):
        return self.title


class Category(models.Model):
    '''
    博客个人文章分类表
    '''
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='blog', to_field='nid')

    def __str__(self):
        return self.title + "->" + self.blog.user.nickname

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'category'
        ordering = ['title']


class Article(models.Model):
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题', max_length=50)
    desc = models.CharField(verbose_name='文章描述', max_length=255)

    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)

    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    category = models.ForeignKey(verbose_name='文章类型', to='Category', to_field='nid', null=True)
    user = models.ForeignKey(verbose_name='所属用户', to='UserInfo', to_field='nid')

    tag = models.ManyToManyField(
        to='Tag',
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )

    def __str__(self):
        return self.title + "-->" + self.user.nickname


class ArticleDetail(models.Model):
    '''
    文章详细表
    '''
    nid = models.AutoField(primary_key=True)
    content = models.TextField(verbose_name='文章内容')
    article = models.OneToOneField(verbose_name='所属文章', to='Article', to_field='nid')

    def __str__(self):
        return self.article.title


class Comment(models.Model):
    '''
    评论数
    '''
    nid = models.BigAutoField(primary_key=True)
    content = models.TextField(verbose_name='评论内容', default="")
    comment_data = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid')
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid')

    parent_comment = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论')

    def __str__(self):
        return self.content


class CommentUp(models.Model):
    '''
    点赞表
    '''
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='UserInfo', null=True)
    comment = models.ForeignKey(to='Comment', null=True)


class ArticleUp(models.Model):
    '''
    点赞表
    '''
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='UserInfo', null=True)
    article = models.ForeignKey(to='Article', null=True)


class Tag(models.Model):
    '''
    标签
    '''
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')

    def __str__(self):
        return self.title + "     -->" + self.blog.user.nickname


class Article2Tag(models.Model):
    '''
    文章标签多对多表
    '''
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='文章', to='Article', to_field='nid')
    tag = models.ForeignKey(verbose_name='标签', to='Tag', to_field='nid')

    class Meta:
        unique_together = [
            ('article', 'tag')
        ]

    def __str__(self):
        return self.article.title + "--" + self.tag.title


class SiteCategory(models.Model):
    '''
    网站分类
    '''
    nid = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='网站分类', max_length=32)

    def __str__(self):
        return self.name


class SiteArticlecategory(models.Model):
    '''
    技术分类
    '''
    nid = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='技术分类', max_length=32)
    siteCategory = models.ForeignKey(to='SiteCategory', to_field='nid')

    def __str__(self):
        return self.name
