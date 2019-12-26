"""Score URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from scores import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.Login),
    path('outlogin/', views.OutLogin),
    path('upload/', views.Upload),
    path('uploadfile/', views.Uploadfile),
    path('download/', views.Download),
    path('index/', views.Index),
    path('studentscore/', views.StudentScore),
    path('student/<int:studentid>/', views.StudentID),
    path('updatestudent/<int:studentid>/', views.UpdateStudent),
    path('updatestudentscore/<int:studentid>/', views.UpdateStudentScore),
    path('problemscore/', views.ProblemScore),
    path('knowledge/',views.Knowledge),
    path('updateknowledge/', views.UpdateKnowledge),
    path('addknowledge/', views.AddKnowledge),
    path('queryknowledge/', views.QueryKnowledge),
    path('problem/', views.Problem),
    path('updateproblem/', views.UpdateProblem),
    path('teacher/', views.Teacher),
    path('updateteacher/', views.UpdateTeacher),
    path('updatepassword/', views.UpdatePassword),
    path('intocourse/<str:coursename>/', views.IntoCourse),
    path('addcourse/',views.AddCourse),
    path('delcourse/<str:coursename>/', views.DelCourse),
    path('updatecourse/<str:coursename>/', views.UpdateCourse),
]
