from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import User
from .models import *
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request,"portal/index.html")
    



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "portal/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "portal/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "portal/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "portal/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "portal/register.html")
    

def course_registration(request):
    
    acyear=request.GET.get("acyear")
    semister=request.GET.get("semister")


    allregistration=Registration.objects.all()
    reg_completed=[]
    for j in allregistration:
        reg_completed.append(j.registeredfor.CourseName)
    print(reg_completed) 
    user = request.user
    info = StudentProfile.objects.filter(name=user).first()
    if info is None:
        message="No student profile found."
        return render(request,"portal/error.html",{"message":message})

    else:
        av_course = []
        invalid_course=[]
        course_list = Course.objects.filter(semister=semister,acadamicyear=acyear)
        for i in course_list:
            z=i.courselist.all()
            for reg in z:
                if reg.name==request.user:
                    invalid_course.append(reg.registeredfor)                   
            if i.acadamicyear == info.department.acadamicyear and i not in invalid_course:#and not alrady registered for that course
                av_course.append(i)
    
                        
            print(av_course) 
        if request.method == 'POST':
        
            selected_choices = request.POST.getlist('courses[]')  
            for j in selected_choices:
                items = Course.objects.get(id=j)
                dep = Department.objects.get(dep_name=info.department.dep_name)
                Registration.objects.create(name=request.user, registeredfor=items, department=dep)
                messages.success(request, 'Registration successfully completed!')
                #return render(request, "portal/error.html", {"message":"Registration Successfully Done"})
                return HttpResponseRedirect(reverse("cregistration"))
            

        return render(request, "portal/course_registration.html", {"av_course": av_course,"reg_completed":reg_completed})
    

def convert_to_gpa(score):
    if score >= 90:
        return ("A+", 4.0)
    elif score >= 85:
        return ("A", 4.0)
    elif score >= 80:
        return ("A-", 3.7)
    elif score >= 75:
        return ("B+", 3.3)
    elif score >= 70:
        return ("B", 3.0)
    elif score >= 65:
        return ("B-", 2.7)
    elif score >= 60:
        return ("C+", 2.3)
    elif score >= 50:
        return ("C", 2.0)
    else:
        return ("F", 0.0)


def Assessment(request):
    semister = request.GET.get("semister")
    if semister is None:
        return render(request, "portal/asses.html")
    
    try:
        student = StudentProfile.objects.get(name=request.user)
    except StudentProfile.DoesNotExist:
        return render(request, "portal/error.html", {"message": "No student profile found."})

    
    assessments = student.stu_info.filter(semister=semister)
    if not assessments.exists():
        return render(request, "portal/error.html", {"message": f"Semester {semister} not found for the student."})

    total_weighted_gpa = 0
    total_ects = 0

    for ass in assessments:
        grade_letter, gpa_point = convert_to_gpa(ass.result)
        ass.Grade = grade_letter
        ass.save()
        ects = ass.course.ECTS
        total_weighted_gpa += gpa_point * ects
        total_ects += ects

    sgpa = round(total_weighted_gpa / total_ects, 2) if total_ects else 0.00

    
    semester_result, created = SemesterResult.objects.get_or_create(
        student=student,
        semister=semister,
        defaults={"sgpa": sgpa}
    )
    if not created and semester_result.sgpa != sgpa:
        semester_result.sgpa = sgpa
        semester_result.save()

    return render(request, "portal/asses.html", {
        "student": student,
        "sgpa": sgpa,
        "assessments": assessments,
        "semister": semister  
    })


def Profile(request): 
    profile = StudentProfile.objects.get(name=request.user)
    results = profile.semester_results.all()
    comulative = 0
    sem = len(results)

    for i in results:
        comulative += i.sgpa

    if sem > 0:  
        profile.cgpa = comulative / sem
        profile.cgpa = round(profile.cgpa, 2)
    else:
        profile.cgpa = 0.00 

    profile.save()

    return render(request, "portal/profile.html", {"profile": profile})


def Upload(request):
    profile=StudentProfile.objects.get(name=request.user)
    img=request.GET.get("img")
    profile.image=img
    profile.save()

    return HttpResponse("Upload successfull")




def news_page(request):
    if request.method == 'GET':
        data = []
        for i in Announcement.objects.all():
            data.append({
                'topic': i.topic,
                'date': i.date,
                'message': i.message,
                'image': i.img  
            })
        return JsonResponse(data, safe=False)


def newsdisplay(request):
    return render(request,"portal/news.html")


    









            
        


