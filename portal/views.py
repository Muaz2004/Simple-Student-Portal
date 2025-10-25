from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import User, StudentProfile, Department, Course, Registration, Assesment, SemesterResult, Announcement
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, "portal/index.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

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
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "portal/register.html", {
                "message": "Passwords must match."
            })

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
    acyear = request.GET.get("acyear")
    semister = request.GET.get("semister")

    user = request.user
    profile = StudentProfile.objects.filter(name=user).first()
    if profile is None:
        message = "No student profile found."
        return render(request, "portal/error.html", {"message": message})

    registered_courses = [reg.registeredfor for reg in Registration.objects.filter(name=user)]
    av_course = Course.objects.filter(acadamicyear=acyear, semister=semister).exclude(id__in=[c.id for c in registered_courses])

    if request.method == 'POST':
        selected_choices = request.POST.getlist('courses[]')
        for course_id in selected_choices:
            course = Course.objects.get(id=course_id)
            Registration.objects.create(
                name=request.user,
                registeredfor=course,
                department=profile.department,
                semister=course.semister
            )
        messages.success(request, 'Registration successfully completed!')
        return HttpResponseRedirect(reverse("cregistration"))

    return render(request, "portal/course_registration.html", {
        "av_course": av_course,
        "registered_courses": registered_courses
    })


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
    acadamicyear = request.GET.get("acadamicyear")

    if semister is None or acadamicyear is None:
        return render(request, "portal/asses.html")

    try:
        student = StudentProfile.objects.get(name=request.user)
    except StudentProfile.DoesNotExist:
        return render(request, "portal/error.html", {"message": "No student profile found."})

    assessments = student.stu_info.filter(semister=semister, course__acadamicyear=acadamicyear)
    if not assessments.exists():
        return render(request, "portal/error.html", {"message": f"No results found for Academic Year {acadamicyear}, Semester {semister}."})

    total_weighted_gpa = 0
    total_ects = 0

    for ass in assessments:
        grade_letter, gpa_point = convert_to_gpa(ass.result)
        ass.Grade = grade_letter
        ass.save()
        total_weighted_gpa += gpa_point * ass.course.ECTS
        total_ects += ass.course.ECTS

    sgpa = round(total_weighted_gpa / total_ects, 2) if total_ects else 0.00

    semester_result, created = SemesterResult.objects.get_or_create(
        student=student,
        acadamicyear=acadamicyear,
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
        "semister": semister,
        "acadamicyear": acadamicyear
    })


def Profile(request):
    profile = StudentProfile.objects.get(name=request.user)
    results = profile.semester_results.all()
    total_sgpa = sum([r.sgpa for r in results])
    sem_count = len(results)

    profile.cgpa = round(total_sgpa / sem_count, 2) if sem_count else 0.00
    profile.save()
    return render(request, "portal/profile.html", {"profile": profile})


def Upload(request):
    profile = StudentProfile.objects.get(name=request.user)
    img = request.GET.get("img")
    profile.image = img
    profile.save()
    return HttpResponse("Upload successful")


def news_page(request):
    data = []
    for announcement in Announcement.objects.all():
        data.append({
            "topic": announcement.topic,
            "date": announcement.date,
            "message": announcement.message,
            "image": announcement.img
        })
    return JsonResponse(data, safe=False)


def newsdisplay(request):
    return render(request, "portal/news.html")
