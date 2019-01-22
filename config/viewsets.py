from django.utils import timezone
from rest_framework import viewsets

from datetime import datetime

from config.serializers import StudentSessionSerializer

from afterschool.students.models import StudentSession


class StudentSessionViewSet(viewsets.ModelViewSet):
    queryset = StudentSession.objects.filter(
        start__gt=timezone.make_aware(datetime.today().replace(hour=0, minute=1)), end__isnull=True)
    serializer_class = StudentSessionSerializer

    def get_queryset(self):
        queryset = StudentSession.objects.filter(
            start__gt=timezone.make_aware(datetime.today().replace(hour=0, minute=1)), end__isnull=True)
        search_string = self.request.query_params.get('search', None)
        if search_string is not None:
            return queryset.filter(student__name__contains=search_string)
        else:
            return queryset
