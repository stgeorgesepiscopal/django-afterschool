import csv, calendar, re
from io import TextIOWrapper

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from ..models import StudentSession, Student, ScheduledClass, StudentSessionsGroup
from ..forms import (SessionForm, MultiSessionForm, MultiSessionGradesForm,
                     MultiSessionEndForm, MultiSessionEndStaffForm,
                     WhereIsForm, ImportSchedulesForm,
                     )
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import Http404, HttpResponse

from django.contrib import messages

from django.utils import timezone, dateparse
from django.db import transaction

from django.db.models import Min, Max, Count, Sum

from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta


class SessionListView(ListView):
    model = StudentSession
    template_name = "students/session_list.html"
    paginate_by = 2000
    context_object_name = "session_list"
    allow_empty = True
    page_kwarg = 'page'
    paginate_orphans = 0

    def __init__(self, **kwargs):
        return super(SessionListView, self).__init__(**kwargs)



class SessionDetailView(DetailView):
    model = StudentSession
    template_name = "students/session_detail.html"
    context_object_name = "session"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'

    def __init__(self, **kwargs):
        return super(SessionDetailView, self).__init__(**kwargs)



class SessionCreateView(CreateView):
    model = StudentSession
    form_class = SessionForm
    # fields = ['start', 'end', 'student', 'parent']
    template_name = "students/session_create.html"
    success_url = reverse_lazy("session_list")

    def __init__(self, **kwargs):
        return super(SessionCreateView, self).__init__(**kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(SessionCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("students:session_detail", args=(self.object.pk,))


class SessionUpdateView(UpdateView):
    model = StudentSession
    form_class = SessionForm
    # fields = ['start', 'end', 'student', 'parent']
    template_name = "students/session_update.html"
    initial = {}
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = "session"

    def __init__(self, **kwargs):
        return super(SessionUpdateView, self).__init__(**kwargs)

    def get_object(self, queryset=None):
        obj = super(SessionUpdateView, self).get_object(queryset)
        if obj.end is None:
            if obj.start is not None:
                obj.end = timezone.localtime(obj.start).replace(minute=0, hour=18)
        return obj

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(SessionUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("students:session_detail", args=(self.object.pk,))


class SessionDeleteView(DeleteView):
    model = StudentSession
    template_name = "students/session_delete.html"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = "session"

    def __init__(self, **kwargs):
        return super(SessionDeleteView, self).__init__(**kwargs)

    def get_success_url(self):
        return reverse("students:session_list")


class SessionMultiCreateView(FormView):
    form_class = MultiSessionForm
    template_name = "students/session_create_multiple.html"

    def __init__(self, **kwargs):
        return super(SessionMultiCreateView, self).__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        open_sessions = StudentSession.objects.filter(start__lt=timezone.now().replace(hour=0, minute=1), end__isnull=True)
        for s in open_sessions:
            m = '<b>WARNING:</b> Open session for ' + s.student.name + ' on ' + s.start.strftime('%c')
            m += ' <a href="' + reverse("students:session_update",
                                        args=[s.pk]) + '" class="btn btn-danger btn-sm float-right">Update</a>'
            messages.error(request, m, extra_tags='safe')
        return super(SessionMultiCreateView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        # obj.save()
        return super(SessionMultiCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SessionMultiCreateView, self).get_context_data(**kwargs)
        more_context = {'current_time': datetime.today().strftime('%A, %B %d, %Y')}
        context.update(more_context)
        return context

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Sessions started')
        return reverse("students:session_create_multiple")
        # return reverse("students:session_detail", args=(self.object.pk,))


class SessionMultiCreateGradesView(SessionMultiCreateView):
    form_class = MultiSessionGradesForm

    def get_form_kwargs(self, **kwargs):
        kw = super(SessionMultiCreateView, self).get_form_kwargs(**kwargs)
        kw.update({'grades': self.kwargs['grades']})
        return kw


class SessionMultiEndView(FormView):
    form_class = MultiSessionEndForm
    template_name = "students/session_end_multiple.html"

    def __init__(self, **kwargs):
        return super(SessionMultiEndView, self).__init__(**kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        for s in obj:
            messages.success(self.request, '<h3>Checked out: ' + str(s) + '</h3>', extra_tags='safe')
        return super(SessionMultiEndView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SessionMultiEndView, self).get_context_data(**kwargs)
        more_context = {'current_time': datetime.today().strftime('%A, %B %d, %Y')}
        context.update(more_context)
        return context

    def get_success_url(self):
        return reverse("students:session_end_multiple")


class SessionMultiEndStaffView(SessionMultiEndView):
    form_class = MultiSessionEndStaffForm
    template_name = "students/session_end_multiple.html"

    def __init__(self, **kwargs):
        return super(SessionMultiEndStaffView, self).__init__(**kwargs)

    def get_success_url(self):
        return reverse("students:session_end_multiple_staff")


class SessionTodayView(ListView):
    model = StudentSession
    template_name = "students/session_today.html"
    paginate_by = 2000
    context_object_name = "session_list"
    allow_empty = True
    page_kwarg = 'page'
    paginate_orphans = 0

    def __init__(self, **kwargs):
        return super(SessionTodayView, self).__init__(**kwargs)

    def get_queryset(self):
        # s = super(SessionListView, self).get_queryset()
        return StudentSession.objects.filter(
            start__gt=timezone.make_aware(datetime.today().replace(hour=0, minute=1))).order_by(
            'complete', 'student__grade', 'student__last_name')

    def get_context_data(self, *args, **kwargs):
        ret = super(SessionTodayView, self).get_context_data(*args, **kwargs)
        return ret

    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True):
        return super(SessionTodayView, self).get_paginator(queryset, per_page, orphans=0, allow_empty_first_page=True)


class SessionDayView(SessionTodayView):

    def get_queryset(self):
        try:
            start = dateparse.parse_date(self.request.GET['start'])
        except:
            start = dateparse.parse_date(self.kwargs['start'])
        # print(start)
        return StudentSession.objects.filter(start__date=start).order_by('student__grade', 'student__last_name')

    def get_context_data(self, *args, **kwargs):
        ret = super(SessionTodayView, self).get_context_data(*args, **kwargs)
        #print(ret)
        return ret


class SessionDayGroupView(SessionDayView):
    template_name = "students/sessiongroups_today.html"

    def get_queryset(self):
        try:
            start = dateparse.parse_date(self.request.GET['start'])
        except:
            start = dateparse.parse_date(self.kwargs['start'])
        # print(start)
        return StudentSessionsGroup.objects.filter(date=start).order_by('student__grade', 'student__last_name')


class WhereIsView(FormView):
    # model = Session
    form_class = WhereIsForm
    # fields = ['start', 'end', 'student', 'parent']
    template_name = "students/where_is.html"

    # success_url = reverse_lazy("session_list")

    def __init__(self, **kwargs):
        return super(WhereIsView, self).__init__(**kwargs)

    def form_valid(self, form, **kwargs):
        obj = form.save(commit=False)
        iterobj = iter(obj)
        try:
            messages.info(self.request, '<h4><small>Where is </small>' + obj[
                0].student.name + '<small> at ' + datetime.today().strftime('%-I:%M %p') + '?</small></h4>',
                          extra_tags='safe')
        except:
            messages.error(self.request, 'No scheduled classes')

        for o in iterobj:
            m = f"<span class=\"font-weight-italic\">{o.start.strftime('%-I:%M %p')}-"\
                f"{o.end.strftime('%-I:%M %p')}</span>: {o.course} ({o.teacher}) "\
                f"in <span class=\"font-weight-bold\">{o.room}</span>"
            if o.current:
                messages.success(self.request, f'<h3>{m}</h3>', extra_tags='safe')
            else:
                messages.warning(self.request, m, extra_tags='safe')

        return super(WhereIsView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(WhereIsView, self).get_context_data(**kwargs)
        more_context = {'current_time': timezone.now().strftime('%c')}
        context.update(more_context)
        return context

    def get_success_url(self):
        return reverse("where_is")
        # return reverse("students:session_detail", args=(self.object.pk,))


class ImportSchedulesView(FormView):
    # model = Session
    form_class = ImportSchedulesForm
    # fields = ['start', 'end', 'student', 'parent']
    template_name = "students/import_file.html"

    # success_url = reverse_lazy("session_list")

    def __init__(self, **kwargs):
        return super(ImportSchedulesView, self).__init__(**kwargs)

    def form_valid(self, form, **kwargs):
        ScheduledClass.objects.all().delete()
        # print("delete")
        f = TextIOWrapper(self.request.FILES['csv_file'].file, encoding='utf-8-sig')
        # print("TextIOWrapper")
        reader = csv.DictReader(f)
        # print("reader")
        student_id = 0
        for row in reader:
            if student_id != row['Student Id']:
                student_id = row['Student Id']
                s, _ = Student.objects.get_or_create(pcr_id=row['Student Id'])

            sched, created = ScheduledClass.objects.get_or_create(student=s,
                                                                  weekday=int(row['Day Of Cycle']) - 1,
                                                                  course=row['Course Name'], room=row['Room'],
                                                                  start=datetime.strptime(row['Begin Time'],
                                                                                          "%I:%M %p"),
                                                                  end=datetime.strptime(row['End Time'], "%I:%M %p"), )
            if created:
                sched.teacher = row['Teacher Last Name']
            else:
                sched.teacher = sched.teacher + '/' + row['Teacher Last Name']
            sched.save()
            # print(sched)

        return super(ImportSchedulesView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ImportSchedulesView, self).get_context_data(**kwargs)
        more_context = {'current_time': datetime.today().strftime('%A, %B %d, %Y')}
        context.update(more_context)
        return context

    def get_success_url(self):
        return reverse("students:import_schedules")
        # return reverse("students:session_detail", args=(self.object.pk,))


class ImportStudentsView(FormView):
    # model = Session
    form_class = ImportSchedulesForm
    # fields = ['start', 'end', 'student', 'parent']
    template_name = "students/import_file.html"

    # success_url = reverse_lazy("session_list")
    def form_valid(self, form, **kwargs):

        f = TextIOWrapper(self.request.FILES['csv_file'].file, encoding='utf-8-sig')
        reader = csv.DictReader(f)
        for row in reader:
            if row['Student First Name'] != 'Fahad':
                # name = row['Student First Name'] + ' ' + row['Student Last Name']
                s, created = Student.objects.get_or_create(pcr_id=row['Student Id'], grade=row['Grade Level Num'])
                s.first_name = row['Student First Name']
                s.last_name = row['Student Last Name']
                s.nickname = row['Student Nickname']
                s.pcr_id = row['Student Id']
                s.grade = row['Grade Level Num']
                if row['Student Nickname'] == row['Student First Name'] or '':
                    s.name = row['Student First Name'] + ' ' + row['Student Last Name']
                else:
                    s.name = row['Student First Name'] + ' (' + row['Student Nickname'] + ') ' + row[
                        'Student Last Name']

            s.save()
            # print(row)

        return super(ImportStudentsView, self).form_valid(form)

    def get_success_url(self):
        return reverse("students:import_students")
        # return reverse("students:session_detail", args=(self.object.pk,))


def month_year_generator(start, end):
    date_yielded = start.replace(day=1)
    end = end.replace(day=28)
    while date_yielded < end:
        yield (date_yielded.month, date_yielded.year)
        date_yielded = date_yielded + relativedelta(months=+1)


class SessionCalendarView(TemplateView):
    template_name = "students/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        minmax = StudentSession.objects.aggregate(min=Min('start'), max=Max('start'))
        calendars = []
        ds = []
        for d in StudentSession.objects.values('start__date__year', 'start__date__month', 'start__date__day',
                                        'start__date').annotate(Count('start__date')):
            ds.append((d['start__date__year'], d['start__date__month'], d['start__date__day']))

        def re_sessions(year, month, match):
            # print(year, month, match.group(1))
            # print(ds)
            if match.group(1):
                if (year, month, int(match.group(1))) in ds:
                    return f' p-1"><a href="day/{year}-{month}-{match.group(1)}" class="btn btn-sm btn-info w-100">{match.group(1)}</a><'
            return f' p-1 text-black-50"><div class="w-100 text-center mx-auto"><small>{match.group(1)}</small></div><'

        for month, year in month_year_generator(minmax['min'], minmax['max']):

            cal = calendar.HTMLCalendar()
            html_cal = cal.formatmonth(year, month)
            html_cal = re.sub(f'{year}',f'{year} <a href="export/{month}/{year}" class="text-success"><i class="fal fa-file-spreadsheet"></i></a>',html_cal)
            mapping = [('Mon', 'M'), ('Tue', 'T'), ('Wed', 'W'), ('Thu', 'T'), ('Fri', 'F'), ('Sat', 'S'), ('Sun', 'S')]
            for k, v in mapping:
                html_cal = html_cal.replace(k, v)
            calendars.append(re.sub(r'">(\d+)<', lambda match: re_sessions(year, month, match), html_cal))

        context.update({'calendars': calendars})

        return context


def csv_export(request, month, year):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="afterschool-{month}-{year}.csv"'

    #sessions = StudentSession.objects.filter(start__month=int(month),start__year=int(year)).annotate(Count('student')).annotate(total_duration=Sum('duration'))

    #students = Student.objects.filter(split_billing=False, sessions__start__month=int(month), sessions__start__year=int(year)).annotate(duration_sum=Sum('sessions__duration'), overtime_sum=Sum('sessions__overtime'))

    students = StudentSessionsGroup.objects.\
        filter(date__month=int(month), date__year=int(year), student__split_billing=False).\
        values('student').\
        annotate(duration_sum=Sum('duration'), overtime_sum=Sum('overtime')).\
        values_list('student__first_name', 'student__last_name', 'student__pcr_id',
                    'duration_sum', 'overtime_sum', named=True)

    students_split_ratio = StudentSessionsGroup.objects. \
        filter(date__month=int(month), date__year=int(year), student__split_billing=True, student__parent1_pays__gt=0). \
        values('student'). \
        annotate(duration_sum=Sum('duration'), overtime_sum=Sum('overtime')). \
        values_list('student__first_name', 'student__last_name', 'student__pcr_id',
                    'student__parent1_pays', 'duration_sum', 'overtime_sum', named=True)

    students_split = StudentSessionsGroup.objects.\
        filter(date__month=int(month), date__year=int(year), student__split_billing=True, student__parent1_pays__lt=0).\
        values('student', 'parent').\
        annotate(duration_sum=Sum('duration'), overtime_sum=Sum('overtime')).\
        values_list('student__first_name', 'student__last_name', 'student__pcr_id',
                    'parent', 'duration_sum', 'overtime_sum', named=True)

    writer = csv.writer(response)
    writer.writerow(['Transaction Date', 'Customer ID', 'Student ID', 'Full Name', 'Account ID', 'Account Name', 'Adjustment Code', 'Adjustment Reason', 'Amount', 'Description'])
    # for s in students:
    #     tdate = datetime.now().strftime('%-m/%d/%Y')
    #     cid = ''
    #     sid = s.pcr_id
    #     fullname = s.last_name+', '+s.first_name
    #     accountID = 'Aftercare'
    #     accountName = 'Aftercare'
    #     adjustmentCode = '2'
    #     adjReason = 'Aftercare'
    #     amt = (int(s.duration_sum) * 8) + (int(s.overtime_sum) * 3)
    #     desc = f'Aftercare for {s.first_name}, month of {calendar.month_name[int(month)]}, {year}. {s.duration_sum} hours @ $8/hour.'
    #     if s.overtime_sum > 0:
    #         desc += f'  {s.overtime_sum} minutes of overtime (past 6:05pm) @ $3/minute.'
    #     writer.writerow([tdate, cid, sid, fullname, accountID, accountName, adjustmentCode, adjReason, amt, desc])

    for ss in (students, students_split):
        for s in ss:
            tdate = datetime.now().strftime('%-m/%d/%Y')
            cid = ''
            sid = s.student__pcr_id
            fullname = f'{s.student__last_name}, {s.student__first_name}'
            if 'parent' in s._fields:
                fullname += f' ({s.parent})'
            accountID = 'Aftercare'
            accountName = 'Aftercare'
            adjustmentCode = '2'
            adjReason = 'Aftercare'
            amt = (int(s.duration_sum) * 8) + (int(s.overtime_sum) * 3)
            desc = f'Aftercare for {s.student__first_name}, month of {calendar.month_name[int(month)]}, {year}. '\
                   f'{s.duration_sum} hours @ $8/hour.'
            if s.overtime_sum > 0:
                desc += f'  {s.overtime_sum} minutes of overtime (past 6:05pm) @ $3/minute.'
            writer.writerow([tdate, cid, sid, fullname, accountID, accountName, adjustmentCode, adjReason, amt, desc])

    for s in students_split_ratio:
        parent = 0
        for rate in (s.student__parent1_pays, 100 - s.student__parent1_pays):
            parent += 1
            tdate = datetime.now().strftime('%-m/%d/%Y')
            cid = ''
            sid = f'{s.student__pcr_id}_{parent}'
            fullname = f'{s.student__last_name}, {s.student__first_name}'
            accountID = 'Aftercare'
            accountName = 'Aftercare'
            adjustmentCode = '2'
            adjReason = 'Aftercare'
            amt = round(((int(s.duration_sum) * 8) + (int(s.overtime_sum) * 3)) * (rate / 100), 2)

            desc = f'{rate}% of aftercare for {s.student__first_name},'\
                f' month of {calendar.month_name[int(month)]}, {year}. '\
                f'{s.duration_sum} hours @ $8/hour.'
            if s.overtime_sum > 0:
                desc += f'  {s.overtime_sum} minutes of overtime (past 6:05pm) @ $3/minute.'
            writer.writerow([tdate, cid, sid, fullname, accountID, accountName, adjustmentCode, adjReason, amt, desc])

    return response
