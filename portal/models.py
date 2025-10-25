from django.db import models
from django.contrib.auth.models import User

# -------------------------------
# Department Model
# -------------------------------
class Department(models.Model):
    dep_name = models.CharField(max_length=64)
    acadamicyear = models.IntegerField(default=2024)  # ✅ Added default

    def __str__(self):
        return f"{self.dep_name} ({self.acadamicyear})"


# -------------------------------
# Course Model
# -------------------------------
class Course(models.Model):
    CourseName = models.CharField(max_length=64)
    ECTS = models.IntegerField()
    acadamicyear = models.IntegerField(default=2024)  # ✅ Added default
    semister = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.CourseName} ({self.ECTS} ECTS, Year {self.acadamicyear}, Sem {self.semister})"


# -------------------------------
# Student Profile Model
# -------------------------------
class StudentProfile(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="studentlist")
    image = models.URLField(blank=True)
    cgpa = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.name.username} - {self.department.dep_name}"


# -------------------------------
# Registration Model
# -------------------------------
class Registration(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    registeredfor = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="courselist")
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    acadamicyear = models.IntegerField(default=2024)  # ✅ Added default
    semister = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name.username} registered for {self.registeredfor.CourseName} (Year {self.acadamicyear}, Sem {self.semister})"


# -------------------------------
# Assessment Model
# -------------------------------
class Assesment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="stu_info")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    result = models.FloatField(default=0)
    acadamicyear = models.IntegerField(default=2024)  # ✅ Added default
    semister = models.IntegerField(default=1)
    Grade = models.CharField(max_length=2, default="NG")

    def __str__(self):
        return f"{self.student.name.username} - {self.course.CourseName} ({self.acadamicyear}/{self.semister})"


# -------------------------------
# Semester Result Model
# -------------------------------
class SemesterResult(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="semester_results")
    acadamicyear = models.IntegerField(default=2024)  # ✅ Added default
    semister = models.IntegerField(default=1)
    sgpa = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('student', 'acadamicyear', 'semister')

    def __str__(self):
        return f"{self.student.name.username} - Year {self.acadamicyear}, Sem {self.semister}: SGPA {self.sgpa}"


# -------------------------------
# Announcement Model
# -------------------------------
class Announcement(models.Model):
    topic = models.CharField(max_length=50)
    message = models.CharField(max_length=400)
    date = models.DateField(auto_now=True)
    img = models.URLField(blank=True)

    def __str__(self):
        return f"Announcement on {self.topic}"
