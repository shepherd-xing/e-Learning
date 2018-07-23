from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Course

# Create your views here.
class OwnerMixin():
    '''检索当前用户的对象'''
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerEditMixin():
    def form_valid(self, form):
        form.instance.owner = self.request.user         #保存对象时设置当前用户
        return super.form_valid(form)

class OwnerCourseMixin(OwnerMixin):
    model = Course      #用于queryset的模型，被所有视图使用

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['subject', 'title', 'slug', 'overview']       #构建CreateView和UpdateView视图的模型表单
    success_url = reverse_lazy('manage_course_list')        #表单提交成功后，重定向
    template_name = 'courses/manage/course/form.html'

class ManageCourseListView(OwnerCourseMixin, ListView):
    '''列出用户创建的课程'''
    template_name = 'courses/manage/course/list.html'

class CourseCreateView(OwnerCourseEditMixin, CreateView):
    pass

class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    pass

class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('manage_course_list')        #删除后重定向













