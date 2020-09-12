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


class CheckoutSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    timestamp = serializers.DateTimeField()
    student__name = serializers.CharField()
    student__grade = serializers.IntegerField()
    student__gradestr = serializers.CharField()

    class Meta:
        model = Checkout
        fields = ('pk', 'timestamp', 'student__name', 'student__grade', 'student__gradestr')


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
