from django.conf.urls import url
from django.urls import path
from ..views import (SessionListView, SessionCreateView, SessionDetailView,
                     SessionUpdateView, SessionDeleteView, SessionMultiCreateView,
                     SessionMultiEndView, SessionMultiEndStaffView, SessionTodayView, WhereIsView, SessionMultiCreateHistoricalView,
                     SessionMultiCreateGradesView, ImportSchedulesView, ImportStudentsView, ScanView, CheckoutView,
                     )
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^create/$',  # NOQA
        login_required(SessionCreateView.as_view()),
        name="session_create"),

    url(r'^createmulti/$',  # NOQA
        login_required(SessionMultiCreateView.as_view()),
        name="session_create_multiple"),

    url(r'^createhistorical/$',  # NOQA
        login_required(SessionMultiCreateHistoricalView.as_view()),
        name="session_create_historical"),

    url(r'^import/schedules/$',  # NOQA
        login_required(ImportSchedulesView.as_view()),
        name="import_schedules"),

    url(r'^import/students/$',  # NOQA
        login_required(ImportStudentsView.as_view()),
        name="import_students"),

    path('createmulti/<grades>',  # NOQA
         login_required(SessionMultiCreateGradesView.as_view()),
         name="session_create_multiple_grades"),

    url(r'^endmulti/$',  # NOQA
        SessionMultiEndView.as_view(),
        name="session_end_multiple"),

    url(r'^scan/$',  # NOQA
        ScanView.as_view(),
        name="scan"),
    
    url(r'^carpool/$',  # NOQA
        CheckoutView.as_view(),
        name="carpool"),

    url(r'^endmultistaff/$',  # NOQA
        login_required(SessionMultiEndStaffView.as_view()),
        name="session_end_multiple_staff"),

    url(r'^today/$',  # NOQA
        SessionTodayView.as_view(),
        name="session_today"),

    url(r'^(?P<pk>\d+)/update/$',
        login_required(SessionUpdateView.as_view()),
        name="session_update"),

    url(r'^(?P<pk>\d+)/delete/$',
        login_required(SessionDeleteView.as_view()),
        name="session_delete"),

    url(r'^(?P<pk>\d+)/$',
        SessionDetailView.as_view(),
        name="session_detail"),

    url(r'^$',
        SessionListView.as_view(),
        name="session_list"),
]
