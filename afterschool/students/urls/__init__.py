from django.conf.urls import include, url

app_name="afterschool.students"

urlpatterns = [

    url(r'^days_of_the_week/', include('afterschool.students.urls.dayof_week_urls')),  # NOQA
    url(r'^students/', include('afterschool.students.urls.student_urls')),
    url(r'^families/', include('afterschool.students.urls.family_urls')),
    url(r'^sessions/', include('afterschool.students.urls.session_urls')),
]
