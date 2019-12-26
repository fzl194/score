from scores.models import Teacher
from scores.models import Course
from scores.modelsexp import *

'''
教师登录：
参数：教师名称name 密码password
返回值：True，False
'''
def Check_Teacher1(name, password):
    a = Teacher.objects.filter(name = name)
    if a.count() != 1:
        return (False, "用户名称不存在")    #用户名称不存在
    a = a[0]
    if password != a.password:
        return (False, "密码错误")    #密码错误
    return (True, "密码正确")


def Check_Teacher(name, password):
    a = Teacher.objects.filter(name = name)
    if not a.count():
        raise ModelNotFoundError    #教师名称不存在
    a = a[0]
    if password != a.password:
        raise PermissionDeniedError    #密码错误

'''
教师登录时选择课程名称
参数：教师名称name 课程名称coursename
'''
def Check_Teacher_Course(name, coursename):
    a = Course.objects.filter(teacher__name = name).filter(name = coursename)
    if a.count() == 0:
        return False
    return True



'''
教师注册：
参数：教师名称name 密码password 真实姓名truename 邮箱email
返回值：True，False
注意：教师名称唯一，注意判断
'''
def Add_Teacher(name, password, truename, email, phone, sex):
    pass


'''
返回该教师所有课程
参数：教师名称name
返回值：返回一个List<Course>
'''
def Get_Teacher_Course(name):
    all = Course.objects.filter(teacher__name = name).order_by('id')
    ans = []
    for item in all:
        ans.append(item.name)
    return ans

'''
给教师添加一门课程
参数：教师名称teachername，课程名coursename
返回值：添加成功：True，添加失败：False
注意：数据库中设置课程名全局唯一，添加前判断一下是否存在相同课程名称，或者添加捕获异常
'''
def Add_Teacher_Course(teachername, coursename):
    if Teacher.objects.filter(name = teachername).count() == 0:
        return
    if Course.objects.filter(teacher__name = teachername, name = coursename).count() != 0:
        return
    now = Course()
    a=Teacher.objects.filter(name = teachername)[0]
    now.teacher = a
    now.name = coursename
    now.save()

'''
根据教师名称，返回教师对象
'''
def Get_Teacher(teachername):
    a = Teacher.objects.filter(name = teachername)
    if a.count() == 0:
        return None
    return a[0]

def Update_Teacher(teachername, truename, email, phone, sex):
    a = Teacher.objects.filter(name = teachername)
    if a.count() == 0:
        return
    a = a[0]
    if truename != None:
        a.truename = truename
    if email != None:
        a.email = email
    if phone != None:
        a.phone = phone
    if sex != None:
        a.sex = sex
    a.save()

def Update_Possword(teachername, password):
    a = Teacher.objects.filter(name = teachername)
    if a.count() == 0:
        return
    a = a[0]
    a.newpassword = password
    a.save()
