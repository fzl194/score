from django.db import models

# Create your models here.

#教师表
class Teacher(models.Model):
    name = models.CharField(max_length=100, verbose_name = '用户名')
    password = models.CharField(max_length=100, verbose_name = '密码')
    newpassword = models.CharField(max_length=100, blank = True, null = True, default="", verbose_name = '新密码')
    truename = models.CharField(max_length=100, blank = True, verbose_name = '真实姓名', null = True)
    email = models.CharField(max_length=100, blank = True, verbose_name="邮箱", null = True)
    
    class Meta:
        #数据库表格名称
        db_table = 'Teacher'
        verbose_name = '教师表'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
    '''
    后台只允许修改newpassword，数据库表格中已添加触发器：更新newpassword时，将password更新，并且newpassword赋值成空
    '''

#课程表
class Course(models.Model):
    #教师外键：一门课属于一位教师
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,  verbose_name = '教师')
    name = models.CharField(max_length=100, verbose_name = '课程名')
    def Get_Teacher_Truename(self):
        return self.teacher.truename
    Get_Teacher_Truename.short_description = '开课教师'
    class Meta:
        db_table = 'Course'
        verbose_name = '课程表'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Course_Problem(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name = '课程')
    problem = models.CharField(max_length=100, verbose_name = '课程题目')
    scoresum = models.IntegerField(default=0, verbose_name = '题目总分')
    course_knowledge = models.ManyToManyField('Course_Knowledge', through='Problem_Knowledge', verbose_name = '题目对应知识点')
    class Meta:
        db_table = 'Course_Problem'
        verbose_name = '课程题目表'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.course.name + " " + self.problem

class Course_Knowledge(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name = '课程')
    knowledge = models.CharField(max_length=100, verbose_name = '课程知识点')
    class Meta:
        db_table = 'Course_Knowledge'
        verbose_name = '课程知识点表'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.course.name + " " + self.knowledge

class Problem_Knowledge(models.Model):
    course_problem = models.ForeignKey(Course_Problem, on_delete=models.CASCADE, verbose_name = '课程题目')
    course_knowledge = models.ForeignKey(Course_Knowledge, on_delete=models.CASCADE, verbose_name = '课程知识点')
    def Get_course_problem(self):
        return self.course_problem.problem
    Get_course_problem.short_description = '题目'
    def Get_course_knowledge(self):
        return self.course_knowledge.knowledge
    Get_course_knowledge.short_description = '知识点'
    def Get_Course(self):
        return self.course_problem.course.name
    Get_Course.short_description = '课程'
    class Meta:
        db_table = 'Problem_Knowledge'
        verbose_name = '题目知识点表'
        verbose_name_plural = verbose_name
        unique_together = ('course_problem', 'course_knowledge',)
    def __str__(self):
        return self.course_problem.problem + " " + self.course_knowledge.knowledge + " " + self.course_problem.course.name

class Student(models.Model):
    studentid = models.CharField(max_length=100, verbose_name = '学号')
    studentname = models.CharField(max_length=100,null = True, blank = True, verbose_name='姓名')
    email = models.CharField(max_length=100,null = True, blank = True, verbose_name='邮箱')
    phone = models.CharField(max_length=100,null=True, blank=True, verbose_name='手机')
    choices_gender = (
        (0,'男'),
        (1,'女'),
        (2,'未知')
    )
    sex = models.IntegerField(choices=choices_gender, default=2, verbose_name='性别')
    course_problem = models.ManyToManyField(Course_Problem, through='Student_Course_Problem', verbose_name = '学生题目分数')
    class Meta:
        db_table = 'Student'
        verbose_name = '学生表'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.studentid

class Student_Course_Problem(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name = '学号')
    course_problem = models.ForeignKey(Course_Problem, on_delete=models.CASCADE, verbose_name = '课程题目')
    score = models.IntegerField(default=0, verbose_name = '学生题目分数')
    class Meta:
        db_table = 'Student_Course_Problem'
        verbose_name = '学生题目表'
        verbose_name_plural = verbose_name
        unique_together = ('student', 'course_problem',)
    def __str__(self):
        return self.student.studentid+" "+self.course_problem.problem