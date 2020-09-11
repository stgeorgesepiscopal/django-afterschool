from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response

from datetime import datetime

from config.serializers import StudentSessionSerializer, StudentSerializer, StaffSerializer

from afterschool.students.models import StudentSession, Student, Staff, Scan


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


class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.filter(grade__lt=9)
    serializer_class = StudentSerializer

    def get_queryset(self):
        queryset = Student.objects.filter(grade__lt=9)
        search_string = self.request.query_params.get('search', None)
        if search_string is not None:
            return queryset.filter(name__contains=search_string)
        else:
            return queryset


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    def get_queryset(self):
        queryset = Staff.objects.all()
        search_string = self.request.query_params.get('search', None)
        if search_string is not None:
            return queryset.filter(name__icontains=search_string)
        else:
            return queryset


class PeopleViewSet(viewsets.ViewSet):

    def list(self, request):
        staff_queryset = Staff.objects.all()
        student_queryset = Student.objects.filter(grade__lt=9)

        search_string = request.query_params.get('search', None)
        if search_string is not None:
            staff_queryset = staff_queryset.filter(name__icontains=search_string)
            student_queryset = student_queryset.filter(name__icontains=search_string)
        
        carpool = request.query_params.get('carpool', None)
        if carpool is not None:
            student_queryset = Student.objects.filter(grade__lt=9).exclude(checkouts__timestamp__gt=timezone.make_aware(datetime.today().replace(hour=0, minute=1))).order_by('last_name','grade')

        staff_serializer = StaffSerializer(staff_queryset, many=True)
        student_serializer = StudentSerializer(student_queryset, many=True)

        return Response({'staff': staff_serializer.data, 'students': student_serializer.data})

