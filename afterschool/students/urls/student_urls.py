from django.conf.urls import url
from ..views import (StudentListView, StudentCreateView, StudentDetailView,
                     StudentUpdateView, StudentDeleteView,
                     StaffListView, StaffCreateView, StaffDetailView,
                     StaffUpdateView, StaffDeleteView,)
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
    
    url(r'^staffcreate/$',  # NOQA
        login_required(StaffCreateView.as_view()),
        name="staff_create"),

    url(r'^(?P<pk>\d+)/staffupdate/$',
        login_required(StaffUpdateView.as_view()),
        name="staff_update"),

    url(r'^(?P<pk>\d+)/staffdelete/$',
        login_required(StaffDeleteView.as_view()),
        name="staff_delete"),

    url(r'^(?P<pk>\d+)/staff$',
        StaffDetailView.as_view(),
        name="staff_detail"),

    url(r'^staff$',
        StaffListView.as_view(),
        name="staff_list"),
]
