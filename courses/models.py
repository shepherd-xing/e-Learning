from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
# Create your models here.
class Subject(models.Model):
    title = models.CharField('标题', max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    class Meta:
        ordering = ('title',)
    def __str__(self):
        return self.title

class Course(models.Model):
    owner = models.ForeignKey(User, verbose_name='教师', related_name='courses_created')
    subject = models.ForeignKey(Subject, verbose_name='主题', related_name='courses')
    title = models.CharField('标题', max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField('概述')
    created = models.DateTimeField('创建时间', auto_now_add=True)
    students = models.ManyToManyField(User, related_name='courses_joined', blank=True)
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return self.title

class Module(models.Model):
    '''课程单元'''
    course = models.ForeignKey(Course, verbose_name='课程', related_name='modules')
    title = models.CharField('标题', max_length=200)
    description = models.TextField('描述', blank=True)
    order = OrderField(verbose_name='排序', blank=True, for_fields=['course'])
    class Meta:
        ordering = ['order']
    def __str__(self):
        return '{}. {}'.format(self.order, self.title)

class Content(models.Model):
    module = models.ForeignKey(Module, verbose_name='课程单元', related_name='contents')
    content_type = models.ForeignKey(ContentType, verbose_name='内容类型',
                                     limit_choices_to={'model__in': ('text', 'video', 'image', 'file')})
    object_id = models.PositiveIntegerField('关联模型的主键')
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(verbose_name='排序', blank=True, for_fields=['module'])
    class Meta:
        ordering = ['order']

class ItemBase(models.Model):
    owner = models.ForeignKey(User, verbose_name='教师', related_name='%(class)s_related')
    title = models.CharField('标题', max_length=250)
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        abstract = True
    def __str__(self):
        return self.title

    def render(self):
        return render_to_string('courses/content/{}.html'.format(self._meta.model_name), {'item':self})

class Text(ItemBase):
    content = models.TextField('文本内容')

class File(ItemBase):
    file = models.FileField('文件', upload_to='files')

class Image(ItemBase):
    file = models.FileField('图片', upload_to='images')

class Video(ItemBase):
    url = models.URLField('视频URL')























































































