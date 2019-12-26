from scores.models import *


'''
添加一位同学
参数：学生学号studentid
'''
def Add_Student(studentid):
    student=Student.objects.filter(studentid=studentid)
    if student.count() == 0:
        student=Student()
        student.studentid = studentid
        student.save()


'''
返回某位同学的某门课的分数详情
参数：学生学号studentid，课程名称coursename
返回：两个值
    第一个是总分
    第二个返回一个类似这样结构的分数 [("选择题1",2),("选择题2",2),("选择题3",2)...]
'''
def Get_Student_Course(studentid, coursename):
    all = Student_Course_Problem.objects.filter(student__studentid = studentid, course_problem__course__name = coursename).order_by('course_problem__id')
    ans = []
    tot = 0
    for item in all:
        now = []
        now.append(item.course_problem.problem)
        now.append(item.score)
        tot += item.score
        ans.append(now)
    return (tot, ans)


'''
在coursename内 模糊查询关键字：studentid 
返回查询到的学生studentid
'''
def Get_Student_byid(studentid, coursename):
    all = Student.objects.filter(course_problem__course__name=coursename).distinct().order_by('id')
    all = all.filter(studentid__contains=studentid).order_by('id')
    ans = []
    for item in all:
        ans.append(item.studentid)
    return ans

def Get_Student_information(studentid):
    ans = Student.objects.filter(studentid=studentid)
    if ans.count() == 0:
        return None
    return ans[0]

'''
添加一个学生
'''
def Update_Student(studentid,email,phone,sex,studentname):
    student=Student.objects.filter(studentid=studentid)
    if student.count():
        student = student[0]
        student.email=email
        student.phone=phone
        student.sex=sex
        student.studentname=studentname
        student.save()
    else:
        student=Student()
        student.studentid=studentid
        student.email=email
        student.phone=phone
        student.sex=sex
        student.studentname=studentname
        student.save()