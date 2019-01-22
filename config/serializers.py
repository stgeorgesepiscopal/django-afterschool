from rest_framework import serializers

from afterschool.students.models import StudentSession, Student

class StudentSerializer(serializers.Serializer):
    name = serializers.CharField()

class StudentSessionSerializer(serializers.HyperlinkedModelSerializer):
    student = StudentSerializer()
    class Meta:
        model = StudentSession
        fields = ('pk', 'student',)
