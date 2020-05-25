from rest_framework import routers

from config.viewsets import StudentSessionViewSet, StaffViewSet, StudentsViewSet, PeopleViewSet

router = routers.DefaultRouter()

router.register("opensessions", StudentSessionViewSet)
router.register("staff", StaffViewSet)
router.register("students", StudentsViewSet)
router.register("people", PeopleViewSet, base_name="api")
