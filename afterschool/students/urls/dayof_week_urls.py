from django.conf.urls import url
from ..views import (DayofWeekListView, DayofWeekCreateView, DayofWeekDetailView,
                     DayofWeekUpdateView, DayofWeekDeleteView)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^create/$',  # NOQA
        login_required(DayofWeekCreateView.as_view()),
        name="dayof_week_create"),

    url(r'^(?P<pk>\d+)/update/$',
        login_required(DayofWeekUpdateView.as_view()),
        name="dayof_week_update"),

    url(r'^(?P<pk>\d+)/delete/$',
        login_required(DayofWeekDeleteView.as_view()),
        name="dayof_week_delete"),

    url(r'^(?P<pk>\d+)/$',
        DayofWeekDetailView.as_view(),
        name="dayof_week_detail"),

    url(r'^$',
        DayofWeekListView.as_view(),
        name="dayof_week_list"),
]
