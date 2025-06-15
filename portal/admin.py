from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(StudentProfile)
admin.site.register(Course)
admin.site.register(Registration)
admin.site.register(Department)
admin.site.register(Assesment)
admin.site.register(SemesterResult)
admin.site.register(Announcement)

