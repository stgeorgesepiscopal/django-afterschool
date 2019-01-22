from rest_framework import routers

from config.viewsets import StudentSessionViewSet

router = routers.DefaultRouter()

router.register("opensessions", StudentSessionViewSet)
