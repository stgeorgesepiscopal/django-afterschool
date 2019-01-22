from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.contrib.auth.decorators import login_required

from afterschool.students.views.session_views import (SessionMultiEndView,
                                                      SessionMultiCreateView, SessionTodayView, SessionDayView,
                                                      WhereIsView, SessionDayGroupView,
                                                      SessionCalendarView, csv_export
                                                      )

from config.routers import router

urlpatterns = [
                  path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
                  path(
                      "about/",
                      TemplateView.as_view(template_name="pages/about.html"),
                      name="about",
                  ),
                  # Django Admin, use {% url 'admin:index' %}
                  path(settings.ADMIN_URL, admin.site.urls),
                  # User management
                  path(
                      "users/",
                      include("afterschool.users.urls", namespace="users"),
                  ),
                  path("accounts/", include("allauth.urls")),
                  path("students/", include("afterschool.students.urls", namespace="students")),
                  path("kiosk",  # NOQA
                       SessionMultiEndView.as_view(),
                       name="kiosk"),
                  path("start",  # NOQA
                       login_required(SessionMultiCreateView.as_view()),
                       name="start"),
                  path("today",  # NOQA
                       login_required(SessionTodayView.as_view()),
                       name="today"),
                  path("day",
                       login_required(SessionDayGroupView.as_view()),
                       name="day"),
                  path("day/<start>",  # NOQA
                       login_required(SessionDayGroupView.as_view()),
                       name="day_hardlink"),
                  path("allsessions/<start>",  # NOQA
                       login_required(SessionDayView.as_view()),
                       name="daysessions_hardlink"),
                  path("export/<month>/<year>",  # NOQA
                       login_required(csv_export),
                       name="export"),
                  path("whereis",  # NOQA
                       WhereIsView.as_view(),
                       name="where_is"),
                  path("cal",
                       login_required(SessionCalendarView.as_view()),
                       name="calendar"),
                  # Your stuff: custom urls includes go here
                  path("api-auth/", include('rest_framework.urls')),
                  path("api/", include(router.urls)),
              ] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
