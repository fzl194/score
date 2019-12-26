from scores.models import *

'''
返回某门课程的题目
参数：课程名称coursename
返回值：一个类似这样结构的分数 [("选择题1","选择题1内容",2),("选择题2","选择题2内容",2),("选择题3",2)...]
'''
def Get_Course_Problem(coursename):
    all = Course_Problem.objects.filter(course__name = coursename).order_by('id')
    ans = []
    for item in all:
        now = []
        now.append(item.problem)
        now.append(item.problem_detail)
        now.append(item.scoresum)
        ans.append(now)
    return ans

'''
查询某门课程是否存在某道题目
参数：课程名称coursename，题目名称problem
返回值：存在True，不存在False
'''
def Exist_Course_Problem(coursename, problem):
    if Course_Problem.objects.filter(course__name = coursename, problem = problem).count() == 0:
        return False
    else:
        return True

'''
查询某门课程某道题目的总分
参数：课程名称coursename，题目名称problem
返回值：存在True，不存在False
'''
def Get_Course_Problem_Score(coursename, problem):
    a = Course_Problem.objects.filter(course__name = coursename, problem = problem)
    if a.count() == 0:
        return 0
    else:
        return a[0].scoresum

'''
给某门课程添加一道题目
参数：课程名称coursename，题目名称problem，题目描述：problem_detail，题目分数：scoresum
'''
def Add_Course_Problem(coursename, problem, scoresum):
    if Exist_Course_Problem(coursename, problem) == True:
        now = Course_Problem.objects.filter(course__name = coursename, problem = problem)[0]
        now.scoresum = scoresum
        now.save()
    else:
        course_problem=Course_Problem()
        course_problem.problem=problem
        course_problem.scoresum=scoresum
        course_problem.course=Course.objects.filter(name=coursename)[0]
        course_problem.save()

'''
给某门课程添加一道题目
参数：课程名称coursename，题目名称problem，题目描述：problem_detail，题目分数：scoresum
'''
def Add_Course_Problem1(coursename, problem, scoresum,problem_detail):
    if problem == "":
        return
    if Exist_Course_Problem(coursename, problem) == True:
        now = Course_Problem.objects.filter(course__name = coursename, problem = problem)[0]
        now.scoresum = scoresum
        now.problem_detail=problem_detail
        now.save()
    else:
        course_problem=Course_Problem()
        course_problem.problem=problem
        course_problem.scoresum=scoresum
        course_problem.problem_detail=problem_detail
        course_problem.course=Course.objects.filter(name=coursename)[0]
        course_problem.save()


'''
返回某门课程的总分
参数：课程名称coursename
返回值：课程总分
'''
def Get_Course_Scoresum(coursename):
    all = Get_Course_Problem(coursename)
    ans = 0
    for item in all:
        ans += item[2]
    return ans


'''
返回某门课程的所有同学
参数：课程名称coursename
返回值：同学名称
'''
def Get_Course_Student(coursename):
    all = Student.objects.filter(course_problem__course__name=coursename).distinct().order_by('id')
    ans = []
    for item in all:
        ans.append(item.studentid)
    return ans



'''
返回某位同学，某门课程，某道题目的分数
参数：课程名称coursename，学生学号studentid，题目名称problem
返回值：某位同学，某门课程，某道题目的分数
'''
def Get_Course_Problem_Student(coursename, problem, studentid):
    course_problem = Course_Problem.objects.filter(course__name = coursename, problem = problem)[0]
    ans = Student_Course_Problem.objects.filter(student__studentid = studentid, course_problem = course_problem)
    if ans.count() == 0:
        return 0
    return ans[0].score

'''
添加某位同学，某门课程，某道题目的分数
参数：课程名称coursename，学生学号studentid，题目名称problem
返回值：某位同学，某门课程，某道题目的分数
'''
def Add_Course_Problem_Student(coursename, problem, studentid, score):
    course_problem = Course_Problem.objects.filter(course__name = coursename, problem = problem)[0]
    student = Student.objects.filter(studentid = studentid)[0]
    ans = Student_Course_Problem.objects.filter(student = student, course_problem = course_problem)
    if ans.count() == 0:
        now = Student_Course_Problem()
        now.student = student
        now.course_problem = course_problem
        now.score = score
        now.save()
    else:
        ans = ans[0]
        ans.score = score
        ans.save()

'''
返回某门课程的所有成绩表
'''
def Get_Course_AllScore(coursename, problems, students):
    ans = []
    for student in students:
        now = []
        for problem in problems:
            now.append(Get_Course_Problem_Student(coursename, problem[0], student))
        ans.append(now)
    return ans


'''
返回某门课程每个人的总分
参数：课程名称coursename
返回值：每个人的分数
只需要分数，目的是为了统计最大值、最小值等
'''
def Get_Course_Sum_Score(coursename):
    all = Get_Course_AllScore(coursename,Get_Course_Problem(coursename),Get_Course_Student(coursename))
    ans = []
    for item in all:
        ans.append(sum(item))
    return ans


'''
返回某门课程某道题目的分数list
参数：课程名称coursename 问题名称problem
返回值：每个人的分数
只需要分数，目的是为了统计最大值、最小值等
'''
def Get_CourseScore_byproblem(coursename, problem):
    all = Student_Course_Problem.objects.filter(course_problem__course__name = coursename, course_problem__problem = problem)
    ans = []
    for item in all:
        ans.append(item.score)
    return ans


'''
根据课程查找教师
'''
def Get_Teacher(coursename):
    a = Course.objects.filter(name = coursename)
    if a.count() == 0:
        return None
    return a[0].teacher

'''
查询课程是否存在
'''
def Exist_Course(coursename):
    if Course.objects.filter(name = coursename).count() != 0:
        return True
    return False


'''
删除课程
'''
def Del_Course(coursename):
    a = Course.objects.filter(name = coursename)
    if a.count() != 0:
        a = a[0]
        a.delete()

def Update_Course(coursename, newname):
    a = Course.objects.filter(name = newname)
    if a.count() != 0:
        return False
    a = Course.objects.filter(name = coursename)
    if a.count() == 0:
        return False
    a = a[0]
    a.name = newname
    a.save()
    return True
