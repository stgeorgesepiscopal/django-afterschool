from rest_framework import serializers

from afterschool.students.models import StudentSession, Student, Staff, Checkout


class StudentSerializer(serializers.Serializer):
    name = serializers.CharField()
    pk = serializers.IntegerField()
    grade = serializers.IntegerField()
    gradestr = serializers.CharField()

    class Meta:
        model = Student
        fields = ('pk', 'name', 'grade','gradestr')


class CheckoutSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField()
    timestamp = serializers.DateTimeField(format="%-I:%M")
    student = StudentSerializer(read_only=True)

    class Meta:
        model = Checkout
        fields = ('pk', 'timestamp', 'student')


class StudentSimpleSerializer(serializers.Serializer):
    name = serializers.CharField()


class StaffSerializer(serializers.Serializer):
    name = serializers.CharField()
    pk = serializers.IntegerField()

    class Meta:
        model = Staff
        fields = ('pk', 'name',)


class StudentSessionSerializer(serializers.HyperlinkedModelSerializer):
    student = StudentSimpleSerializer()
    class Meta:
        model = StudentSession
        fields = ('pk', 'student',)
