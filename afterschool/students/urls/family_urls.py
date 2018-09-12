from django.conf.urls import url
from ..views import (FamilyListView, FamilyCreateView, FamilyDetailView,
                     FamilyUpdateView, FamilyDeleteView)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^create/$',  # NOQA
        login_required(FamilyCreateView.as_view()),
        name="family_create"),

    url(r'^(?P<pk>\d+)/update/$',
        login_required(FamilyUpdateView.as_view()),
        name="family_update"),

    url(r'^(?P<pk>\d+)/delete/$',
        login_required(FamilyDeleteView.as_view()),
        name="family_delete"),

    url(r'^(?P<pk>\d+)/$',
        FamilyDetailView.as_view(),
        name="family_detail"),

    url(r'^$',
        FamilyListView.as_view(),
        name="family_list"),
]
