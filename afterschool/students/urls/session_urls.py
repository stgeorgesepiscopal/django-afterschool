from django.conf.urls import url
from ..views import (SessionListView, SessionCreateView, SessionDetailView,
                     SessionUpdateView, SessionDeleteView, SessionMultiCreateView, 
                     SessionMultiEndView, SessionTodayView, WhereIsView)
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^create/$',  # NOQA
        login_required(SessionCreateView.as_view()),
        name="session_create"),

    url(r'^createmulti/$',  # NOQA
        login_required(SessionMultiCreateView.as_view()),
        name="session_create_multiple"),

    url(r'^endmulti/$',  # NOQA
        SessionMultiEndView.as_view(),
        name="session_end_multiple"),

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
