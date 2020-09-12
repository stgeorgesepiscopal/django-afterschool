from rest_framework import routers

from config.viewsets import StudentSessionViewSet, StaffViewSet, StudentsViewSet, PeopleViewSet, CheckoutsViewSet

router = routers.DefaultRouter()

router.register("opensessions", StudentSessionViewSet)
router.register("staff", StaffViewSet)
router.register("students", StudentsViewSet)
router.register("checkouts", CheckoutsViewSet)
router.register("people", PeopleViewSet, base_name="api")
