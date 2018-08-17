from bootstrap_datepicker_plus import TimePickerInput, DateTimePickerInput

from django import forms
from django.utils import timezone
from .models import DayofWeek, Student, Family, Session, ScheduledClass

from datetime import datetime, timedelta

import logging
logger = logging.getLogger(__name__)

def ceil_dt(dt, delta):
    if timezone.is_naive(dt):
        return dt + (datetime.min - dt) % delta
    else:
        return dt + (datetime.min - timezone.make_naive(dt)) % delta

def floor_dt(dt, delta):
    return ceil_dt(dt, delta) - delta

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
        fields = ['name', 'grade', 'schedule']
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
        model = Session
        fields = ['start', 'end', 'student', 'parent']
        exclude = []
        widgets = {
            'start': DateTimePickerInput(options={'sideBySide':True}).start_of('session'),
            'end': DateTimePickerInput(options={'sideBySide':True}).end_of('session'),
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
                #'inline': True,
                'format': 'LT',
                })
        )
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.all())


    def __init__(self, *args, **kwargs):
        super(MultiSessionForm, self).__init__(*args, **kwargs)
        self.fields["students"].initial=(
            Student.objects.filter(schedule__day__in=[str(timezone.now().weekday())]).values_list('id', flat=True)
            )
        self.fields["students"].queryset=Student.objects.exclude(sessions__start__gt=timezone.now().replace(hour=0,minute=1))
        self.fields["time"].initial=floor_dt(datetime.today(),timedelta(minutes=15)).strftime('%X')

    def save(self, commit=True):
        #print(self.cleaned_data)
        rightnow = datetime.today()
        #formtime = self['time']
        #print(formtime)
        rightnow = timezone.make_aware(rightnow.replace(minute=self.cleaned_data['time'].minute,hour=self.cleaned_data['time'].hour,second=0,microsecond=0))
        #print(rightnow)
        for s in self.cleaned_data['students']:
            ses = Session.objects.create(start=rightnow,student=s)
            s.save()
        return self
        #return super(SessionForm, self).save(commit)

class MultiSessionEndForm(forms.Form):
    #time = forms.TimeField()
    sessions = forms.ModelMultipleChoiceField(queryset=Session.objects.all())
    parent = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(MultiSessionEndForm, self).__init__(*args, **kwargs)
        self.fields["sessions"].queryset=Session.objects.filter(start__gt=timezone.now().replace(hour=0,minute=1),end__isnull=True)
        #self.fields["time"].initial=floor_dt(datetime.today(),timedelta(minutes=15)).strftime('%X')

    def save(self, commit=True):
        #print(self.cleaned_data)
        rightnow = ceil_dt(timezone.now(),timedelta(minutes=15))
        #formtime = self['time']
        #print(formtime)
        #rightnow = rightnow.replace(minute=self.cleaned_data['time'].minute,hour=self.cleaned_data['time'].hour,second=0,microsecond=0)
        #print(rightnow)
        for s in self.cleaned_data['sessions']:
            s.end = rightnow
            s.parent = self.cleaned_data['parent']
            s.save()
        return self
        #return super(SessionForm, self).save(commit)

class WhereIsForm(forms.Form):
    #time = forms.TimeField()
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.all())

    def __init__(self, *args, **kwargs):
        super(WhereIsForm, self).__init__(*args, **kwargs)
        self.fields["students"].queryset=Student.objects.filter(grade__gt=4).order_by('name')
        #self.fields["time"].initial=floor_dt(datetime.today(),timedelta(minutes=15)).strftime('%X')

    def save(self, commit=True):
        #print(self.cleaned_data)
        #rightnow = ceil_dt(timezone.now(),timedelta(minutes=15))
        #formtime = self['time']
        #print(formtime)
        #rightnow = rightnow.replace(minute=self.cleaned_data['time'].minute,hour=self.cleaned_data['time'].hour,second=0,microsecond=0)
        #print(rightnow)
        now = datetime.now()
        for s in self.cleaned_data['students']:
            try:
                scheduled_class = ScheduledClass.objects.get(student=s,start__lte=timezone.localtime().time(),end__gte=timezone.localtime().time(),weekday=timezone.now().weekday())
            except:
                try:
                    scheduled_class = ScheduledClass.objects.get(student=s,start__lte=(timezone.localtime()+timedelta(minutes=5)).time(),end__gte=(timezone.localtime()+timedelta(minutes=5)).time(),weekday=timezone.now().weekday())
                except: 
                    scheduled_class = 'Unknown'                
        return scheduled_class
        #return super(SessionForm, self).save(commit)

class StudentExportForm(forms.Form):
    #time = forms.TimeField()
    sessions = forms.ModelMultipleChoiceField(queryset=Session.objects.all())
    parent = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(StudentExportForm, self).__init__(*args, **kwargs)
        self.fields["sessions"].queryset=Session.objects.filter(start__gt=datetime.today().replace(hour=0,minute=1),end__isnull=True)
        #self.fields["time"].initial=floor_dt(datetime.today(),timedelta(minutes=15)).strftime('%X')

    def save(self, commit=True):
        #print(self.cleaned_data)
        rightnow = ceil_dt(timezone.now(),timedelta(minutes=15))
        #formtime = self['time']
        #print(formtime)
        #rightnow = rightnow.replace(minute=self.cleaned_data['time'].minute,hour=self.cleaned_data['time'].hour,second=0,microsecond=0)
        #print(rightnow)
        for s in self.cleaned_data['sessions']:
            s.end = rightnow
            s.parent = self.cleaned_data['parent']
            #s.save()
        return self
        #return super(SessionForm, self).save(commit)
