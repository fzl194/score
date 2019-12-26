from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt 
from django.http import FileResponse
from django.contrib import messages

from scores import teacherdb
from scores import coursedb
from scores import studentdb
from scores import knowledgedb
from scores import date
from scores.modelsexp import *

# Create your views here.


'''
用户登录
URL：/login/
GET方法：返回登录界面
POST方法：判断True Or False
'''
@csrf_exempt 
def Login(request):
    Map={}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        course = request.POST.get('course')
        try:
            teacherdb.Check_Teacher(username, password)
            request.session['teachername'] = username
            if course != None:
                if teacherdb.Check_Teacher_Course(username, course) == True:
                    request.session['course'] = course
                    return HttpResponseRedirect("/index/")
            return HttpResponseRedirect("/teacher/")
        except ModelNotFoundError:
            Map['error'] = '用户名不存在'
        except PermissionDeniedError:
            Map['error'] = '密码错误'
    return render(request, 'sign_in.html', Map)



'''
退出登录
URL：/outlogin/
清空session
'''
def OutLogin(request):
    request.session.flush()
    return HttpResponseRedirect("/login/")



'''
上传
URL：/upload/
显示成绩详细表格
'''
def Upload(request):
    if 'course' not in request.session.keys():
        messages.success(request, "先选择课程")
        return HttpResponseRedirect("/teacher/")
    Map = {}
    coursename = request.session['course']

    #题目表problemtable         编号  题目  题目总分
    problems = coursedb.Get_Course_Problem(coursename)
    problemtable = []
    ID = 1
    for item in problems:
        now = []
        now.append(ID)
        now.append(item[0])
        now.append(item[2])
        problemtable.append(now)
        ID += 1
    Map['problemtable'] = problemtable


    #分数表的表头scoretablehead
    scoretablehead = []
    scoretablehead.append('编号')
    scoretablehead.append('学号')
    for item in problems:
        scoretablehead.append(item[0])
    scoretablehead.append('总分')
    Map['scoretablehead'] = scoretablehead


    #分数表的内容score
    students = coursedb.Get_Course_Student(coursename)
    score = coursedb.Get_Course_AllScore(coursename,problems,students)
    scoretable = []
    ID = 1
    for item in score:
        now = []
        now.append(ID)
        now.append(students[ID - 1])
        for tmp in item:
            now.append(tmp)
        now.append(sum(item))
        scoretable.append(now)
        ID += 1
    Map['scoretable'] = scoretable
    return render(request, 'upload.html', Map)

import random
import string
def randstr(num):
    salt = ''.join(random.sample(string.ascii_letters + string.digits, num))
    return salt
'''
上传文件
导入成绩
URL：uploadfile
'''
@csrf_exempt
def Uploadfile(request):
    if 'course' not in request.session.keys():
        messages.success(request, "先选择课程")
        return HttpResponseRedirect("/teacher/")
    Map = {}
    coursename = request.session['course']
    if request.method == 'POST':
        #获取文件存入file中
        file_obj = request.FILES.get("fileupload")
        if file_obj == None:
            return HttpResponseRedirect('/upload/')
        filename = randstr(10) + ".csv"
        with open('static/file/' + filename, 'wb') as f:
            for line in file_obj.chunks():
                f.write(line)
        f.close()

        #读文件 找出题目和题目分值
        f = open('static/file/' + filename, encoding='UTF-8-sig')
        lines = f.readlines()
        head = lines[0]
        problemhead = []
        problemscore = []
        table = []
        for every in lines:
            now = every.strip().split(',')
            if now[0].encode('utf-8').decode('GBK')  == '学号'.encode('utf-8').decode('GBK') :
                problemhead = now
            elif now[0] == '0':
                problemscore = now
            else:
                table.append(now)
        #题目和题目分值不能一一对应，直接return
        if len(problemhead) == 0 or len(problemscore) == 0 or len(problemscore) != len(problemhead):
            return HttpResponseRedirect('/upload/')
        #在数据库中插入题目
        number = len(problemhead) - 2
        for i in range(1, number + 1):
            coursedb.Add_Course_Problem(coursename, problemhead[i], problemscore[i])
        
        #在数据库中插入学号
        for every in table:
            studentdb.Add_Student(every[0])
            for i in range(1, number + 1):
                coursedb.Add_Course_Problem_Student(coursename, problemhead[i], every[0], every[i])
        
        return HttpResponseRedirect('/upload/')
        
'''
下载模板
'''
@csrf_exempt 
def Download(request):
    if 'course' not in request.session.keys():
        messages.success(request, "先选择课程")
        return HttpResponseRedirect("/teacher/")
    file = open('static/file/std.csv', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="std.csv"'
    return response


'''
初始化界面
绘制柱状图
选择小题进行数据分析
'''
@csrf_exempt
def Index(request):
    if 'course' not in request.session.keys():
        messages.success(request, "先选择课程")
        return HttpResponseRedirect("/teacher/")
    Map = {}
    
    #总分展示
    coursename = request.session['course']
    allscore = coursedb.Get_Course_Sum_Score(coursename)
    if len(allscore) == 0:
        return render(request, "index.html", Map)
    allscore.sort()
    sumscore = coursedb.Get_Course_Scoresum(coursename)
    score = []
    score.append(sumscore)
    score.append(date.List_Avg(allscore))
    score.append(len(allscore))
    score.append(allscore[-1])
    score.append(allscore[0])
    score.append(date.List_Mid(allscore))
    score.append(date.List_Std(allscore))
    score.append(date.List_Var(allscore))
    
    #十等分
    scoreinterval = []
    nowscore = int(sumscore + 9) // 10
    j = 0
    jige = 0
    n = len(allscore)
    for i in range(10):
        if i == 0:
            L = 0
        else:
            L = i * nowscore + 1
        R = (i + 1) * nowscore
        if R > sumscore:
            R = sumscore
        number = 0
        while j < n and allscore[j] <= R:
            j += 1
            number += 1
        if i >= 6:
            jige += number
        now = [L, R, number]
        scoreinterval.append(now)
        if R == sumscore:
            break
    score.append('{:.2f}%'.format(100*jige/n))
    Map['score'] = score
    Map['scoreinterval'] = scoreinterval

    problems = coursedb.Get_Course_Problem(coursename)
    if len(problems) == 0:
        return render(request, "index.html", Map)

    #小题展示
    Map['problems'] = problems
    selects = problems[0][0]
    if request.method == 'POST':
        if request.POST.get('option') != None:
            selects = request.POST.get('option')
    Map['selects'] = selects

    allscore = coursedb.Get_CourseScore_byproblem(coursename, selects)
    sumscore = coursedb.Get_Course_Problem_Score(coursename, selects)
    score = []
    if len(allscore) != 0:
        allscore.sort()
        score.append(sumscore)
        score.append(date.List_Avg(allscore))
        score.append(len(allscore))
        score.append(allscore[-1])
        score.append(allscore[0])
        score.append(date.List_Mid(allscore))
        score.append(date.List_Std(allscore))
        score.append(date.List_Var(allscore))
    Map['score1'] = score
    #十等分
    j = 0
    n = len(allscore)
    scoreinterval = []
    number = 0
    while j < n and allscore[j] == 0:
        j += 1
        number += 1
    scoreinterval.append([0,0,number])
    nowscore = int(sumscore + 9) // 10
    for i in range(10):
        L = i * nowscore + 1
        R = (i + 1) * nowscore
        if R > sumscore:
            R = sumscore
        number = 0
        while j < n and allscore[j] <= R:
            j += 1
            number += 1
        now = [L, R, number]
        scoreinterval.append(now)
        if R == sumscore:
            break
    Map['scoreinterval1'] = scoreinterval
    return render(request, "index.html", Map)


'''按照学号来排序'''
def cmp1(a):
    return a[1]
'''按照总分排序'''
def cmp2(a):
    return a[2]
'''成绩表，可查找学号，可排序'''
@csrf_exempt
def StudentScore(request):
    if 'course' not in request.session.keys():
        messages.success(request, "先选择课程")
        return HttpResponseRedirect("/teacher/")
    Map = {}
    coursename = request.session['course']
    students = coursedb.Get_Course_Student(coursename)
    studentscore = []
    allscore = []
    ID = 1
    for item in students:
        now = []
        now.append(ID)
        ID += 1
        now.append(item)
        nowscore = studentdb.Get_Student_Course(item, coursename)[0]
        now.append(nowscore)
        allscore.append(nowscore)
        studentscore.append(now)
    Order = date.List_Sort(allscore)
    for item in studentscore:
        item.append(Order[item[2]])
        if item[2] < 60:
            item.append('D')
        elif item[2] < 75:
            item.append('C')
        elif item[2] < 90:
            item.append('B')
        else:
            item.append('A')
    sortstudentid = 0
    sortscore = 0
    studentscore.sort(key=cmp2, reverse=True)        
    if request.method == 'POST':
        if request.POST.get('studentid') != None:
            tmp = request.POST.get('studentid')
            new = []
            for every in studentscore:
                if tmp in every[1]:
                    new.append(every)
            studentscore = new
    else:
        if request.GET.get('sortstudentid') != None:
            sortstudentid = int(request.GET.get('sortstudentid'))
            if sortstudentid == 0 or sortstudentid == 2:
                sortstudentid = 1
                studentscore.sort(key=cmp1)
            else:
                sortstudentid = 2
                studentscore.sort(key=cmp1, reverse=True)
        if request.GET.get('sortscore') != None:
            sortscore = int(request.GET.get('sortscore'))
            if sortscore == 0 or sortscore == 2:
                sortscore = 1
                studentscore.sort(key=cmp2)
            else:
                sortscore = 2
                studentscore.sort(key=cmp2, reverse=True)
    Map['sortstudentid'] = sortstudentid
    Map['sortscore'] = sortscore
    ID = 1
    for item in studentscore:
        item[0] = ID
        ID += 1
    Map['studentscore'] = studentscore
    return render(request, "studentscore.html", Map)


'''
根据studentid，显示学生详细信息
'''
@csrf_exempt
def StudentID(request, studentid):
    if 'course' not in request.session.keys():
        messages.success(request, "先选择课程")
        return HttpResponseRedirect("/teacher/")
    Map = {}
    coursename = request.session['course']
    thisstudent = studentdb.Get_Student_information(studentid)
    student = []
    student.append(thisstudent.studentid)
    student.append(thisstudent.studentname)
    student.append(thisstudent.email)
    student.append(thisstudent.phone)
    student.append(thisstudent.sex)
    thisstudentscore = studentdb.Get_Student_Course(studentid, coursename)
    thisstudentproblem = coursedb.Get_Course_Problem(coursename)
    table = []
    ID = 1
    for i in range(len(thisstudentproblem)):
        now = []
        now.append(ID)
        now.append(thisstudentscore[1][i][0])
        tmp = knowledgedb.Get_Knowledge_BY_Problem(coursename, thisstudentscore[1][i][0])
        ccc = ""
        first = True
        for cnt in tmp:
            if first:
                first = False
            else:
                ccc += ","
            ccc += cnt
        now.append(ccc)
        now.append(thisstudentscore[1][i][1])
        now.append(thisstudentproblem[i][2])
        ID += 1
        table.append(now)
    Map['sum'] = thisstudentscore[0]
    Map['table'] = table
    Map['student'] = student
    table1 = []
    knowledge = knowledgedb.Get_Course_Knowledge(coursename)
    ID = 1
    for item in knowledge:
        now = []
        now.append(ID)
        ID += 1
        now.append(item)
        tmp = knowledgedb.Get_Problem_BY_Knowledge(coursename, item)
        ccc = ""
        first = True
        for cnt in tmp:
            if first:
                first = False
            else:
                ccc += ","
            ccc += cnt
        now.append(ccc)
        now.append(knowledgedb.Get_Knowledge_Score_Student(coursename, item, studentid))
        now.append(knowledgedb.Get_Knowledge_Score(coursename, item))
        table1.append(now)
    Map['table1'] = table1
    return render(request, 'student.html', Map)

'''
更新学生基本信息
'''
@csrf_exempt
def UpdateStudent(request, studentid):
    if 'course' not in request.session.keys():
        messages.success(request, "先选择课程")
        return HttpResponseRedirect("/teacher/")
    Map = {}
    coursename = request.session['course']
    if request.method == "POST":
        studentname = request.POST.get('studentname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        sex = request.POST.get('sex')
        studentdb.Update_Student(studentid, email, phone, sex, studentname)
    return HttpResponseRedirect('/student/'+str(studentid)+'/')

'''
更新学生分数
'''
@csrf_exempt
def UpdateStudentScore(request, studentid):
    if 'course' not in request.session.keys():
        messages.success(request, "先选择课程")
        return HttpResponseRedirect("/teacher/")
    Map = {}
    coursename = request.session['course']
    if request.method == "POST":
        problems = coursedb.Get_Course_Problem(coursename)
        for item in problems:
            now = request.POST.get(item[0])
            if now != None:
                coursedb.Add_Course_Problem_Student(coursename, item[0], studentid, now)
    return HttpResponseRedirect('/student/'+str(studentid)+'/')


'''
显示各个题目的详细分数
'''
def ProblemScore(request):
    if 'course' not in request.session.keys():
        messages.success(request, "先选择课程")
        return HttpResponseRedirect("/teacher/")
    Map = {}
    coursename = request.session['course']
    return render(request, 'problem.html', Map)

'''
返回知识点表格
'''
def GetTable(a, coursename):
    knowledges = knowledgedb.Get_Course_Knowledge(coursename)
    all = []
    ID = 1
    for item in knowledges:
        now = []
        now.append(ID)
        now.append(item)
        now.append(knowledgedb.Get_Knowledge_Score(coursename, item))
        s = ""
        problem = knowledgedb.Get_Problem_BY_Knowledge(coursename, item)
        first = True
        for tmp in problem:
            if first:
                first = False
            else:
                s += ', '
            s += tmp
        now.append(s)
        ID += 1
        all.append(now)
    ans = []
    for every in all:
        if a in every[1] or a in every[2]:
            ans.append(every)
    return ans


@csrf_exempt
def Knowledge(request):
    if 'course' not in request.session.keys():
        messages.success(request, "先选择课程")
        return HttpResponseRedirect("/teacher/")
    Map = {}
    coursename = request.session['course']
    knowledge = knowledgedb.Get_Course_Knowledge(coursename)
    Map['knowledge'] = knowledge
    Map['problems'] = coursedb.Get_Course_Problem(coursename)
    if len(knowledge) != 0:
        Map['problem'] = knowledgedb.Get_Problem_BY_Knowledge(coursename, knowledge[0])
        Map['optionknowledge'] = knowledgedb.Get_a_Course_Knowledge(coursename, knowledge[0])
        Map['table'] = GetTable("", coursename)
    if request.method == "POST":
        if request.POST.get('knowledge') != None:
            Map['table'] = GetTable(request.POST.get('knowledge'), coursename)
    return render(request, 'knowledge.html', Map)


@csrf_exempt
def UpdateKnowledge(request):
    if 'course' not in request.session.keys():
        messages.success(request, "先选择课程")
        return HttpResponseRedirect("/teacher/")
    Map = {}
    coursename = request.session['course']
    if request.method == "POST":
        #a = request.POST.getlist('problems')
        query = request.POST.get('query')
        update = request.POST.get('update')
        if query != None:
            optionknowledge = request.POST.get('optionknowledge')
            knowledge = knowledgedb.Get_Course_Knowledge(coursename)
            Map['knowledge'] = knowledge
            Map['problems'] = coursedb.Get_Course_Problem(coursename)
            problem = knowledgedb.Get_Problem_BY_Knowledge(coursename, optionknowledge)
            Map['problem'] = problem
            Map['optionknowledge'] = knowledgedb.Get_a_Course_Knowledge(coursename, optionknowledge)
            #return HttpResponse(Map['knowledge_detail'])
            Map['table'] = GetTable("", coursename)
            return render(request, 'knowledge.html', Map)
        elif update != None:
            optionknowledge = request.POST.get('optionknowledge')
            knowledge_detail = request.POST.get('knowledge_detail')
            problems = request.POST.getlist('problems')
            if optionknowledge != None and knowledge_detail != None and problems != None:
                    
                knowledgedb.Add_Course_Knowledge(coursename, optionknowledge, knowledge_detail)
                knowledgedb.DelKnowledgeProblem(coursename, optionknowledge)
                for item in problems:
                    knowledgedb.Add_Problem_Knowledge(coursename, item, optionknowledge)
    return HttpResponseRedirect('/knowledge/')
        

@csrf_exempt
def AddKnowledge(request):
    if 'course' not in request.session.keys():
        messages.success(request, "先选择课程")
        return HttpResponseRedirect("/teacher/")
    Map = {}
    coursename = request.session['course']
    if request.method == 'POST':
        knowledge = request.POST.get('knowledge')
        knowledge_detail = request.POST.get('knowledge_detail')
        if len(knowledge) != 0:
            knowledgedb.Add_Course_Knowledge(coursename, knowledge, knowledge_detail)
    return HttpResponseRedirect("/knowledge/")

@csrf_exempt
def QueryKnowledge(request):
    pass




'''
返回知识点表格
'''
def GetTable1(a, coursename):
    problem = coursedb.Get_Course_Problem(coursename)
    all = []
    ID = 1
    for item in problem:
        now = []
        now.append(ID)
        now.append(item[0])
        now.append(item[2])
        s = ""
        Knowledge = knowledgedb.Get_Knowledge_BY_Problem(coursename, item[0])
        first = True
        for tmp in Knowledge:
            if first:
                first = False
            else:
                s += ', '
            s += tmp
        now.append(s)
        ID += 1
        all.append(now)
    ans = []
    for every in all:
        if a in every[1] or a in every[3]:
            ans.append(every)
    return ans


@csrf_exempt
def Problem(request):
    if 'course' not in request.session.keys():
        messages.success(request, "先选择课程")
        return HttpResponseRedirect("/teacher/")
    Map = {}
    coursename = request.session['course']
    problem = coursedb.Get_Course_Problem(coursename)
    Map['problem'] = problem
    Map['knowledges'] = knowledgedb.Get_Course_Knowledge(coursename)
    if len(problem) != 0:
        Map['optionproblem'] = knowledgedb.Get_a_Course_Problem(coursename, problem[0][0])
        Map['knowledge'] = knowledgedb.Get_Knowledge_BY_Problem(coursename, problem[0][0])
        Map['table'] = GetTable1("", coursename)
    if request.method == "POST":
        if request.POST.get('problem') != None:
            Map['table'] = GetTable1(request.POST.get('problem'), coursename)
    return render(request, 'problem.html', Map)


@csrf_exempt
def UpdateProblem(request):
    if 'course' not in request.session.keys():
        messages.success(request, "先选择课程")
        return HttpResponseRedirect("/teacher/")
    Map = {}
    coursename = request.session['course']
    if request.method == "POST":
        query = request.POST.get('query')
        update = request.POST.get('update')
        if query != None:
            optionproblem = request.POST.get('optionproblem')
            problem = coursedb.Get_Course_Problem(coursename)
            Map['problem'] = problem
            Map['knowledges'] = knowledgedb.Get_Course_Knowledge(coursename)
            Map['optionproblem'] = knowledgedb.Get_a_Course_Problem(coursename, optionproblem)
            Map['knowledge'] = knowledgedb.Get_Knowledge_BY_Problem(coursename, optionproblem)
            Map['table'] = GetTable1("", coursename)
            return render(request, 'problem.html', Map)
        elif update != None:
            optionproblem = request.POST.get('optionproblem')
            score = request.POST.get('score')
            problem_detail = request.POST.get('problem_detail')
            knowledges = request.POST.getlist('knowledges')
            if score == "" or score == None:
                score = 0
            if optionproblem != None and score != None:
                coursedb.Add_Course_Problem1(coursename, optionproblem, score, problem_detail)
                knowledgedb.DelProblemKnowledge(coursename, optionproblem)
                for item in knowledges:
                    knowledgedb.Add_Problem_Knowledge(coursename, optionproblem, item)
    return HttpResponseRedirect('/problem/')


'''
登录后自动跳转，默认显示该页面
'''
@csrf_exempt
def Teacher(request):
    if 'teachername' not in request.session.keys():
        messages.success(request, "请先登录")
        return HttpResponseRedirect("/login/")
    teachername = request.session['teachername']
    Map = {}
    teacher = teacherdb.Get_Teacher(teachername)
    Map['teacher'] = teacher
    course = teacherdb.Get_Teacher_Course(teachername)
    ID = 1
    table = []
    for item in course:
        now=[]
        now.append(ID)
        now.append(item)
        ID += 1
        table.append(now)
    Map['course'] = table
    return render(request, 'teacher.html', Map)


'''
更新教师基本信息
'''

@csrf_exempt
def UpdateTeacher(request):
    if 'teachername' not in request.session.keys():
        messages.success(request, "请先登录")
        return HttpResponseRedirect("/login/")
    teachername = request.session['teachername']
    teacher = teacherdb.Get_Teacher(teachername)
    if request.method == "POST":
        truename = request.POST.get('truename')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        sex = request.POST.get('sex')
        teacherdb.Update_Teacher(teachername, truename, email, phone, sex)
    return HttpResponseRedirect('/teacher/')

@csrf_exempt
def UpdatePassword(request):
    if 'teachername' not in request.session.keys():
        messages.success(request, "请先登录")
        return HttpResponseRedirect("/login/")
    teachername = request.session['teachername']
    if request.method == "POST":
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        password3 = request.POST.get('password3')
        if password1 != None and password1 != "" and password2 != None and password2 != "" and password3 != None and password3 != "":
            if teacherdb.Check_Teacher1(teachername, password1)[0] == True:
                if password2 == password3:
                    teacherdb.Update_Possword(teachername, password2)
                    messages.success(request,"修改成功")
                else:
                    messages.success(request,"输入错误")
            else:
                messages.success(request,"密码错误")
    return HttpResponseRedirect('/teacher/')

'''
进入课程
'''
@csrf_exempt
def IntoCourse(request, coursename):
    if 'teachername' not in request.session.keys():
        messages.success(request, "请先登录")
        return HttpResponseRedirect("/login/")
    teachername = request.session['teachername']
    if teacherdb.Check_Teacher_Course(teachername, coursename) == False:
        return HttpResponseRedirect('/teacher/')
    request.session['course'] = coursename
    return HttpResponseRedirect('/index/')

'''
添加课程
'''
@csrf_exempt
def AddCourse(request):
    if 'teachername' not in request.session.keys():
        return HttpResponse("无权限")
    teachername = request.session['teachername']
    if request.method == "POST":
        a = request.POST.get('coursename')
        if a != None and a != "":
            if coursedb.Exist_Course(a) == True:
                messages.success(request, "课程名称已存在")
            else:
                messages.success(request, "添加成功")
                teacherdb.Add_Teacher_Course(teachername, a)

    return HttpResponseRedirect('/teacher/')

@csrf_exempt
def DelCourse(request, coursename):
    if 'teachername' not in request.session.keys():
        return HttpResponse("无权限")
    if request.method == "POST":
        coursedb.Del_Course(coursename)
    return HttpResponseRedirect('/teacher/')

@csrf_exempt
def UpdateCourse(request, coursename):
    if 'teachername' not in request.session.keys():
        return HttpResponse("无权限")
    if request.method == "POST":
        newname = request.POST.get('newname')
        if newname != "" and newname != None and newname != coursename:
            if coursedb.Update_Course(coursename, newname) == False:
                messages.success(request, "课程名称已存在，修改失败")
            else:
                request.session['course'] = newname

    return HttpResponseRedirect('/teacher/')
def page_not_found(request):
    return HttpResponseRedirect('/login/')

