from scores.models import *

'''
添加或者更新一个知识点
'''
def Add_Course_Knowledge(coursename,knowledge,knowledge_detail):
    course=Course.objects.filter(name=coursename)
    if not course.count():
        return
    course=course[0]
    a=Course_Knowledge.objects.filter(knowledge=knowledge,course=course)
    if a.count():
        a = a[0]
        a.knowledge_detail = knowledge_detail
        a.save()
        return
    course_knowledge=Course_Knowledge()
    course_knowledge.knowledge=knowledge
    course_knowledge.course=course
    course_knowledge.knowledge_detail = knowledge_detail
    course_knowledge.save()

'''
返回所有知识点
'''
def Get_Course_Knowledge(coursename):
    all=Course_Knowledge.objects.filter(course__name=coursename).order_by('id')
    ans = []
    for item in all:
        ans.append(item.knowledge)
    return ans

'''
得到一个课程知识点
'''
def Get_a_Course_Knowledge(coursename,knowledge):
    a=Course_Knowledge.objects.filter(course__name=coursename,knowledge=knowledge)
    if not a.count():
        return None
    return a[0]

'''
获取一个课程题目
'''
def Get_a_Course_Problem(coursename,problem):
    problem=Course_Problem.objects.filter(course__name=coursename,problem=problem)
    if not problem.count():
        return None
    return problem[0]


'''
给课程题目添加一个知识点
'''
def Add_Problem_Knowledge(coursename,problem,knowledge):
    a=Problem_Knowledge.objects.filter(course_knowledge__course__name=coursename,course_knowledge__knowledge=knowledge,course_problem__course__name=coursename,course_problem__problem=problem)
    if a.count():
        return
    problem_knowledge=Problem_Knowledge()
    a = Get_a_Course_Knowledge(coursename,knowledge)
    b = Get_a_Course_Problem(coursename,problem)
    if a != None and b != None:
        problem_knowledge.course_knowledge=a
        problem_knowledge.course_problem=b
        problem_knowledge.save()



'''
查询知识点对应的题目
'''
def Get_Problem_BY_Knowledge(coursename, knowledge):
    all = Problem_Knowledge.objects.filter(course_problem__course__name=coursename,course_knowledge__knowledge = knowledge).order_by('course_problem__id')
    ans = []
    for item in all:
        ans.append(item.course_problem.problem)
    return ans

'''
查询课程题目的知识点
'''
def Get_Knowledge_BY_Problem(coursename,problem):
    all=Problem_Knowledge.objects.filter(course_problem__course__name=coursename,course_problem__problem=problem).order_by('course_knowledge__id')
    ans = []
    for item in all:
        ans.append(item.course_knowledge.knowledge)
    return ans

'''
删除知识点对应的题目
'''
def DelKnowledgeProblem(coursename, knowledge):
    all = Problem_Knowledge.objects.filter(course_problem__course__name=coursename,course_knowledge__knowledge = knowledge)
    all.delete()


'''
删除题目对应的知识点
'''
def DelProblemKnowledge(coursename, problem):
    all = Problem_Knowledge.objects.filter(course_problem__course__name=coursename,course_problem__problem=problem)
    all.delete()


'''
查找知识点对应的分数
'''
def Get_Knowledge_Score(coursename, knowledge):
    all = Problem_Knowledge.objects.filter(course_problem__course__name=coursename, course_knowledge__knowledge=knowledge)
    ans = 0
    for item in all:
        ans += item.course_problem.scoresum
    return ans

def Get_Knowledge_Score_Student(coursename, knowledge, studentid):
    all = Student_Course_Problem.objects.filter(course_problem__course__name=coursename, student__studentid=studentid, course_problem__course_knowledge__knowledge =knowledge).distinct()
    ans = 0
    for item in all:
        ans += item.score
    return ans