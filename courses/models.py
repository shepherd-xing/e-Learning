from django.db import models
from django.contrib.auth.models import User
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
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return self.title

class Module(models.Model):
    '''课程单元'''
    course = models.ForeignKey(Course, verbose_name='课程', related_name='modules')
    title = models.CharField('标签', max_length=200)
    description = models.TextField('描述', blank=True)
    def __str__(self):
        return self.title
















































































