from django.contrib import admin
from scores.models import Teacher
from scores.models import Course
from scores.models import Course_Problem
from scores.models import Course_Knowledge
from scores.models import Problem_Knowledge
from scores.models import Student
from scores.models import Student_Course_Problem
# Register your models here.

admin.site.site_header = "后台管理"
admin.site.site_title = '后台管理'

'''
后台教师表配置
'''
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    #展示教师表字段：ID、用户名
    list_display = ('id', 'name','truename','email','phone','sex')
    #点击id和name进入编辑界面
    list_display_links = ('id', 'name')
    #默认按照id升序
    ordering = ('id',)
    #搜索框：搜索名字、学院
    search_fields=['name','truename','email']
    #关闭顶部action
    actions_on_top = False
    #开启底部action
    actions_on_bottom=True
    #修改列表，此处只允许修改newpassword、和数据库底层触发器配套使用
    fields = ('name', 'newpassword','truename','email','phone','sex')
    #右侧过滤器
    list_filter = ('sex',)



'''
后台课程表配置
'''
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    #展示课程表字段：ID、课程名、开课教师
    list_display = ('id', 'name','Get_Teacher_Truename')
    #点击id和name进入编辑界面
    list_display_links = ('id', 'name')
    #默认按照id升序
    ordering = ('id',)
    #搜索框：搜索名字、学院
    search_fields=['name','teacher__truename']
    #关闭顶部action
    actions_on_top = False
    #开启底部action
    actions_on_bottom=True
    #修改列表
    fields = ('name', 'teacher')

class Problem_Knowledge_AdminLine(admin.TabularInline):
    model = Problem_Knowledge
    list_display = ('course_problem','course_knowledge')
    raw_id_fields =  ('course_problem','course_knowledge')

'''
后台问题表配置
'''
@admin.register(Course_Problem)
class Course_ProblemAdmin(admin.ModelAdmin):
    #展示课程表字段：ID、题目、课程名、题目总分
    list_display = ('id','problem', 'course','scoresum')
    #点击id和name进入编辑界面
    list_display_links = ('id', 'problem')
    #默认按照id升序
    ordering = ('id',)
    #搜索框：搜索题目、课程
    search_fields=['problem','course__name']
    #关闭顶部action
    actions_on_top = False
    #开启底部action
    actions_on_bottom=True
    #修改列表
    fields = ('problem', 'problem_detail','course','scoresum')
    inlines = [
        Problem_Knowledge_AdminLine,
    ]


'''
后台知识点表配置
'''
@admin.register(Course_Knowledge)
class Course_KnowledgeAdmin(admin.ModelAdmin):
    #展示课程表字段：ID、知识点、课程名
    list_display = ('id','knowledge', 'course')
    #点击id和name进入编辑界面
    list_display_links = ('id', 'knowledge')
    #默认按照id升序
    ordering = ('id',)
    #搜索框：搜索名字、学院
    search_fields=['knowledge','course__name']
    #关闭顶部action
    actions_on_top = False
    #开启底部action
    actions_on_bottom=True
    #修改列表
    fields = ('knowledge','knowledge_detail', 'course')


'''
后台题目知识点表配置
'''
@admin.register(Problem_Knowledge)
class Problem_KnowledgeAdmin(admin.ModelAdmin):
    #展示课程表字段：ID、题目、知识点、课程名
    list_display = ('id','Get_course_problem', 'Get_course_knowledge','Get_Course')
    #点击id和name进入编辑界面
    list_display_links = ('id',)
    #默认按照id升序
    ordering = ('id',)
    #搜索框：搜索题目、知识点
    search_fields=['course_problem__problem','course_knowledge__knowledge','course_problem__course__name']
    #关闭顶部action
    actions_on_top = False
    #开启底部action
    actions_on_bottom=True
    #修改列表
    fields = ('course_problem', 'course_knowledge')



class Student_Course_Problem_AdminLine(admin.TabularInline):
    model = Student_Course_Problem
    list_display = ('student','course_problem','score')
    raw_id_fields =  ('student','course_problem')

'''
后台学生表配置
'''
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    #展示课程表字段：ID、题目、知识点、课程名
    list_display = ('id','studentid', 'studentname','email','phone','sex')
    #点击id和name进入编辑界面
    list_display_links = ('id','studentid')
    #默认按照id升序
    ordering = ('id',)
    #搜索框：搜索题目、知识点
    search_fields=['studentid','studentname','email','phone','sex']
    #关闭顶部action
    actions_on_top = False
    #开启底部action
    actions_on_bottom=True
    #修改列表
    fields = ('studentid', 'studentname','email','phone','sex')
    #右侧过滤器
    list_filter = ('sex',)
    inlines = [
        Student_Course_Problem_AdminLine,
    ]



'''
后台学生题目表配置
'''
@admin.register(Student_Course_Problem)
class Student_Course_ProblemAdmin(admin.ModelAdmin):
    #展示课程表字段：ID、题目、知识点、课程名
    list_display = ('id','student', 'course_problem','score')
    #点击id和name进入编辑界面
    list_display_links = ('id',)
    #默认按照id升序
    ordering = ('id',)
    #搜索框：搜索题目、知识点
    search_fields=['student__studentid','course_problem__problem']
    #关闭顶部action
    actions_on_top = False
    #开启底部action
    actions_on_bottom=True

    #修改列表
    fields = ('student', 'course_problem','score')
