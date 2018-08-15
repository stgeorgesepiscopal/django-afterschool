from django.conf.urls import url
from ..views import (StudentListView, StudentCreateView, StudentDetailView,
                     StudentUpdateView, StudentDeleteView)
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^create/$',  # NOQA
        login_required(StudentCreateView.as_view()),
        name="student_create"),

    url(r'^(?P<pk>\d+)/update/$',
        login_required(StudentUpdateView.as_view()),
        name="student_update"),

    url(r'^(?P<pk>\d+)/delete/$',
        login_required(StudentDeleteView.as_view()),
        name="student_delete"),

    url(r'^(?P<pk>\d+)/$',
        StudentDetailView.as_view(),
        name="student_detail"),

    url(r'^$',
        StudentListView.as_view(),
        name="student_list"),
]
