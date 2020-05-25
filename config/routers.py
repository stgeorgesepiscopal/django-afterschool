from rest_framework import routers

from config.viewsets import StudentSessionViewSet, StaffViewSet, StudentsViewSet

router = routers.DefaultRouter()

router.register("opensessions", StudentSessionViewSet)
router.register("staff", StaffViewSet)
router.register("students", StudentsViewSet)
