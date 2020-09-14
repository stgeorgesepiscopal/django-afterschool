from bootstrap_datepicker_plus import TimePickerInput, DateTimePickerInput, DatePickerInput

from django import forms
from django.utils import timezone
from .models import DayofWeek, Student, Family, StudentSession, ScheduledClass, Staff, Scan, Checkout
from .utils import ceil_dt, floor_dt

from django.db.models import Case, Value, When, BooleanField

from datetime import datetime, timedelta

import logging

logger = logging.getLogger(__name__)



class DayofWeekForm(forms.ModelForm):
    class Meta:
        model = DayofWeek
        fields = ['day']
        exclude = []
        widgets = None
        localized_fields = None
        labels = {}
        help_texts = {}
        error_messages = {}

    def __init__(self, *args, **kwargs):
        return super(DayofWeekForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        return super(DayofWeekForm, self).is_valid()

    def full_clean(self):
        return super(DayofWeekForm, self).full_clean()

    def clean_day(self):
        day = self.cleaned_data.get("day", None)
        return day

    def clean(self):
        return super(DayofWeekForm, self).clean()

    def validate_unique(self):
        return super(DayofWeekForm, self).validate_unique()

    def save(self, commit=True):
        return super(DayofWeekForm, self).save(commit)


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'grade', 'schedule', 'split_billing', 'parent1_pays']
        exclude = []
        widgets = None
        localized_fields = None
        labels = {}
        help_texts = {}
        error_messages = {}

    def __init__(self, *args, **kwargs):
        return super(StudentForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        return super(StudentForm, self).is_valid()

    def full_clean(self):
        return super(StudentForm, self).full_clean()

    def clean_name(self):
        name = self.cleaned_data.get("name", None)
        return name

    def clean_grade(self):
        grade = self.cleaned_data.get("grade", None)
        return grade

    def clean(self):
        return super(StudentForm, self).clean()

    def validate_unique(self):
        return super(StudentForm, self).validate_unique()

    def save(self, commit=True):
        return super(StudentForm, self).save(commit)


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'email']
        exclude = []
        widgets = None
        localized_fields = None
        labels = {}
        help_texts = {}
        error_messages = {}

    def __init__(self, *args, **kwargs):
        return super(StaffForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        return super(StaffForm, self).is_valid()

    def full_clean(self):
        return super(StaffForm, self).full_clean()

    def clean_name(self):
        name = self.cleaned_data.get("name", None)
        return name

    def clean(self):
        return super(StaffForm, self).clean()

    def validate_unique(self):
        return super(StaffForm, self).validate_unique()

    def save(self, commit=True):
        return super(StaffForm, self).save(commit)

class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['name']
        exclude = []
        widgets = None
        localized_fields = None
        labels = {}
        help_texts = {}
        error_messages = {}

    def __init__(self, *args, **kwargs):
        return super(FamilyForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        return super(FamilyForm, self).is_valid()

    def full_clean(self):
        return super(FamilyForm, self).full_clean()

    def clean_name(self):
        name = self.cleaned_data.get("name", None)
        return name

    def clean(self):
        return super(FamilyForm, self).clean()

    def validate_unique(self):
        return super(FamilyForm, self).validate_unique()

    def save(self, commit=True):
        return super(FamilyForm, self).save(commit)


class SessionForm(forms.ModelForm):
    class Meta:
        model = StudentSession
        fields = ['start', 'end', 'student', 'parent', 'waive_fees']
        exclude = []
        widgets = {
            'start': DateTimePickerInput(options={'sideBySide': True}).start_of('session'),
            'end': DateTimePickerInput(options={'sideBySide': True}).end_of('session'),
        }
        localized_fields = None
        labels = {}
        help_texts = {}
        error_messages = {}

    def __init__(self, *args, **kwargs):
        return super(SessionForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        return super(SessionForm, self).is_valid()

    def full_clean(self):
        return super(SessionForm, self).full_clean()

    def clean_start(self):
        start = self.cleaned_data.get("start", None)
        return start

    def clean_end(self):
        end = self.cleaned_data.get("end", None)
        return end

    def clean_student(self):
        student = self.cleaned_data.get("student", None)
        return student

    def clean_parent(self):
        parent = self.cleaned_data.get("parent", None)
        return parent

    def clean(self):
        return super(SessionForm, self).clean()

    def validate_unique(self):
        return super(SessionForm, self).validate_unique()

    def save(self, commit=True):
        return super(SessionForm, self).save(commit)


class MultiSessionForm(forms.Form):
    time = forms.TimeField(
        widget=TimePickerInput(options={
            # 'inline': True,
            'format': 'LT',
        })
    )
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.all())

    def __init__(self, *args, **kwargs):
        super(MultiSessionForm, self).__init__(*args, **kwargs)
        self.fields["students"].initial = (
            Student.objects.filter(schedule__day__in=[str(timezone.now().weekday())]).values_list('id', flat=True)
        )
        open_sessions = StudentSession.objects.filter(start__gt=timezone.now().replace(hour=0, minute=1), end__isnull=True)
        self.fields["students"].queryset = Student.objects.exclude(sessions__in=open_sessions).exclude(
            grade__lt=-1).order_by('grade', 'last_name')
        self.fields["time"].initial = floor_dt(datetime.today(), timedelta(minutes=15)).strftime('%X')

    def save(self, commit=True):
        # print(self.cleaned_data)
        rightnow = datetime.today()
        # formtime = self['time']
        # print(formtime)
        rightnow = timezone.make_aware(
            rightnow.replace(minute=self.cleaned_data['time'].minute, hour=self.cleaned_data['time'].hour, second=0,
                             microsecond=0))
        # print(rightnow)
        for s in self.cleaned_data['students']:
            ses = StudentSession.objects.create(start=rightnow, student=s)
            s.save()
        return self
        # return super(SessionForm, self).save(commit)


class MultiSessionGradesForm(MultiSessionForm):

    def __init__(self, *args, **kwargs):
        try:
            grades = [int(x) for x in (kwargs.pop('grades')).split(',')]
        except:
            grades = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8]
        super(MultiSessionGradesForm, self).__init__(*args, **kwargs)
        open_sessions = StudentSession.objects.filter(start__gt=timezone.now().replace(hour=0, minute=1), end__isnull=True)
        self.fields["students"].initial = (
            Student.objects.filter(grade__in=grades, schedule__day__in=[str(timezone.now().weekday())]).values_list(
                'id', flat=True)
        )
        self.fields["students"].queryset = Student.objects.filter(grade__in=grades).exclude(
            sessions__in=open_sessions).order_by('grade', 'last_name')
        if -1 in grades:
            if timezone.localtime().weekday() == 2:
                self.fields["time"].initial = timezone.localtime().replace(hour=14, minute=50).strftime('%X')
            else:
                self.fields["time"].initial = timezone.localtime().replace(hour=15, minute=15).strftime('%X')
        else:
            if timezone.localtime().weekday() == 2:
                self.fields["time"].initial = timezone.localtime().replace(hour=15, minute=10).strftime('%X')
            else:
                self.fields["time"].initial = timezone.localtime().replace(hour=16, minute=00).strftime('%X')



class MultiSessionHistoricalForm(forms.Form):
    date = forms.DateField(
        widget=DatePickerInput()
    )
    start_time = forms.TimeField(
        widget=TimePickerInput(options={
            # 'inline': True,
            'format': 'LT',
        })
    )

    end_time = forms.TimeField(
        widget=TimePickerInput(options={
            # 'inline': True,
            'format': 'LT',
        })
    )

    parent = forms.CharField(label='Pick-up person')

    students = forms.ModelMultipleChoiceField(queryset=Student.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["students"].queryset = Student.objects.all()
        self.fields["start_time"].initial = "16:00:00"
        self.fields["end_time"].initial = "18:00:00"

    def save(self, commit=True):
        # print(self.cleaned_data)
        rightnow = datetime.today()
        # formtime = self['time']
        # print(formtime)
        start = timezone.make_aware(datetime.combine(self.cleaned_data['date'], self.cleaned_data['start_time']))
        end = timezone.make_aware(datetime.combine(self.cleaned_data['date'], self.cleaned_data['end_time']))
        # end = self.cleaned_data['date']
        #timezone.make_aware(
        #    start.replace(minute=self.cleaned_data['start_time'].minute, hour=self.cleaned_data['start_time'].hour, second=0, microsecond=0))
        # timezone.make_aware(end.replace(minute=self.cleaned_data['end_time'].minute, hour=self.cleaned_data['end_time'].hour, second=0, microsecond=0))
        # print(rightnow)
        for s in self.cleaned_data['students']:
            ses = StudentSession.objects.create(start=start, end=end, student=s)
            s.save()
        return self
        # return super(SessionForm, self).save(commit)


class MultiSessionEndForm(forms.Form):
    # time = forms.TimeField()
    sessions = forms.ModelMultipleChoiceField(queryset=StudentSession.objects.all())
    parent = forms.CharField(label='Pick-up person')

    def __init__(self, *args, **kwargs):
        super(MultiSessionEndForm, self).__init__(*args, **kwargs)
        self.fields["sessions"].queryset = StudentSession.objects.filter(
            start__gt=timezone.make_aware(datetime.today().replace(hour=0, minute=1)), end__isnull=True)

    def save(self, commit=True):
        rightnow = ceil_dt(timezone.now(), timedelta(minutes=1))

        student_names = []
        for s in self.cleaned_data['sessions']:
            s.end = rightnow
            s.parent = self.cleaned_data['parent']
            s.save()
            student_names += [s.student.name]
        return student_names


class ScanForm(forms.Form):
    # time = forms.TimeField()
    #student = forms.ModelMultipleChoiceField(queryset=Student.objects.all(), required=False)
    staff = forms.ModelMultipleChoiceField(queryset=Staff.objects.all(), required=False)
    #scanners = forms.ModelMultipleChoiceField(queryset=Staff.objects.all())
    temperature = forms.DecimalField(label='Temperature (°F)')
    # preScreenImage = forms.CharField(label='Screening App Image')
    
    def __init__(self, *args, **kwargs):
        super(ScanForm, self).__init__(*args, **kwargs)
        self.fields["staff"].queryset = Staff.objects.exclude(scans__timestamp__gt=timezone.make_aware(datetime.today().replace(hour=0, minute=1)))

    def save(self, commit=True):
        data = self.cleaned_data
        if data['staff'].count() > 0:
            data['staff'] = data['staff'].first()
        else:
            data['staff'] = None
        
        new_scan = Scan.objects.create(student=None, staff=data['staff'], temperature=data['temperature'], timestamp=timezone.now(), result=0)
        
        new_scan.save()

        try:
            return str(new_scan)
        except Exception as e:
            logger.debug(e)
            return "Scanned"


class CheckoutForm(forms.Form):
    # time = forms.TimeField()
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.exclude(id__in=Checkout.objects.filter(
            timestamp__gt=timezone.make_aware(datetime.today().replace(hour=0, minute=1))).values_list('student', flat=True)), required=False)
    location = forms.TypedChoiceField(label='Location', choices=Checkout.LOCATION_CHOICES)

    def __init__(self, *args, **kwargs):
        location = kwargs.pop('location', 0)
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.fields["students"].queryset = Student.objects.filter(grade__lt=9).exclude(checkouts__timestamp__gt=timezone.make_aware(datetime.today().replace(hour=0, minute=1)))
        self.initial["location"] = location

    def save(self, commit=True):
        data = self.cleaned_data
        sessions = []
        for s in data['students']:
            ses = Checkout.objects.create(timestamp=timezone.now(), student=s, location=data['location'])
            ses.save()
            sessions.append(ses)
        try:
            return sessions
        except Exception as e:
            logger.debug(e)
            return "Scanned"



class MultiSessionEndStaffForm(MultiSessionEndForm):
    time = forms.TimeField(
        widget=TimePickerInput(options={
            # 'inline': True,
            'format': 'LT',
        })
    )
    no_charge = forms.BooleanField(help_text='No charge if session was waiting for official SGES activities', initial=True)

    def __init__(self, *args, **kwargs):
        super(MultiSessionEndStaffForm, self).__init__(*args, **kwargs)
        self.fields["time"].initial = floor_dt(datetime.today(), timedelta(minutes=15)).strftime('%X')
        self.fields["parent"].label = 'Activity/Pick-up person'

    def save(self, commit=True):
        rightnow = datetime.today()
        rightnow = timezone.make_aware(
            rightnow.replace(minute=self.cleaned_data['time'].minute, hour=self.cleaned_data['time'].hour, second=0,
                             microsecond=0))
        student_names = []
        for s in self.cleaned_data['sessions']:
            s.end = rightnow
            s.waive_fees = self.cleaned_data['no_charge']
            s.parent = self.cleaned_data['parent']
            s.save()
            student_names += [s.student.name]
        return student_names


class WhereIsForm(forms.Form):
    # time = forms.TimeField()
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.all())

    def __init__(self, *args, **kwargs):
        super(WhereIsForm, self).__init__(*args, **kwargs)
        self.fields["students"].queryset = Student.objects.filter(grade__gt=4).order_by('name')
        # self.fields["time"].initial=floor_dt(datetime.today(),timedelta(minutes=15)).strftime('%X')

    def save(self, commit=True):
        # print(self.cleaned_data)
        # rightnow = ceil_dt(timezone.now(),timedelta(minutes=15))
        # formtime = self['time']
        # print(formtime)
        # rightnow = rightnow.replace(minute=self.cleaned_data['time'].minute,hour=self.cleaned_data['time'].hour,second=0,microsecond=0)
        # print(rightnow)
        now = datetime.now()
        for s in self.cleaned_data['students']:
            try:
                scheduled_classes = ScheduledClass.objects.filter(
                    # student=s,start__lte=timezone.localtime().time(),
                    student=s,
                    end__gte=(timezone.localtime() + timedelta(minutes=-5)).time(),
                    weekday=timezone.now().weekday()
                ).annotate(current=Case(
                    When(start__lte=timezone.localtime().time(),
                         end__gte=timezone.localtime().time(),
                         then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                )).order_by('start')[:3]
            except:
                try:
                    scheduled_classes = ScheduledClass.objects.filter(
                        student=s,
                        start__lte=(timezone.localtime() + timedelta(minutes=5)).time(),
                        weekday=timezone.now().weekday()
                    ).order_by('start')
                except:
                    scheduled_classes = []
        return scheduled_classes
        # return super(SessionForm, self).save(commit)


class StudentExportForm(forms.Form):
    # time = forms.TimeField()
    sessions = forms.ModelMultipleChoiceField(queryset=StudentSession.objects.all())
    parent = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(StudentExportForm, self).__init__(*args, **kwargs)
        # self.fields["sessions"].queryset=Session.objects.filter(start__gt=datetime.today().replace(hour=0,minute=1),end__isnull=True)
        # self.fields["time"].initial=floor_dt(datetime.today(),timedelta(minutes=15)).strftime('%X')

    def save(self, commit=True):
        # print(self.cleaned_data)
        rightnow = ceil_dt(timezone.now(), timedelta(minutes=15))
        # formtime = self['time']
        # print(formtime)
        # rightnow = rightnow.replace(minute=self.cleaned_data['time'].minute,hour=self.cleaned_data['time'].hour,second=0,microsecond=0)
        # print(rightnow)
        for s in self.cleaned_data['sessions']:
            s.end = rightnow
            s.parent = self.cleaned_data['parent']
            # s.save()
        return self
        # return super(SessionForm, self).save(commit)


class ImportSchedulesForm(forms.Form):
    csv_file = forms.FileField()
