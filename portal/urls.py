from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("cregistration",views.course_registration,name="cregistration"),
    path("asses",views.Assessment,name="asses"),
    path("profile",views.Profile,name="profile"),
    path("upload",views.Upload,name="upload"),
    path("edunews", views.newsdisplay, name="edunews"),
    path("news/", views.news_page, name="news"),
]
