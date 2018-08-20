from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from ..models import Session
from ..forms import SessionForm, MultiSessionForm, MultiSessionEndForm, WhereIsForm
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import Http404

from django.contrib import messages

from django.utils import timezone
from datetime import datetime, timedelta

def ceil_dt(dt, delta):
    if timezone.is_naive(dt):
        return dt + (datetime.min - dt) % delta
    else:
        return dt + (datetime.min - timezone.make_naive(dt)) % delta

def floor_dt(dt, delta):
    return ceil_dt(dt, delta) - delta

class SessionListView(ListView):
    model = Session
    template_name = "students/session_list.html"
    paginate_by = 2000
    context_object_name = "session_list"
    allow_empty = True
    page_kwarg = 'page'
    paginate_orphans = 0

    def __init__(self, **kwargs):
        return super(SessionListView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(SessionListView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(SessionListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return super(SessionListView, self).get_queryset()

    def get_allow_empty(self):
        return super(SessionListView, self).get_allow_empty()

    def get_context_data(self, *args, **kwargs):
        ret = super(SessionListView, self).get_context_data(*args, **kwargs)
        return ret

    def get_paginate_by(self, queryset):
        return super(SessionListView, self).get_paginate_by(queryset)

    def get_context_object_name(self, object_list):
        return super(SessionListView, self).get_context_object_name(object_list)

    def paginate_queryset(self, queryset, page_size):
        return super(SessionListView, self).paginate_queryset(queryset, page_size)

    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True):
        return super(SessionListView, self).get_paginator(queryset, per_page, orphans=0, allow_empty_first_page=True)

    def render_to_response(self, context, **response_kwargs):
        return super(SessionListView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(SessionListView, self).get_template_names()


class SessionDetailView(DetailView):
    model = Session
    template_name = "students/session_detail.html"
    context_object_name = "session"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'

    def __init__(self, **kwargs):
        return super(SessionDetailView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(SessionDetailView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(SessionDetailView, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(SessionDetailView, self).get_object(queryset)

    def get_queryset(self):
        return super(SessionDetailView, self).get_queryset()

    def get_slug_field(self):
        return super(SessionDetailView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(SessionDetailView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(SessionDetailView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(SessionDetailView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(SessionDetailView, self).get_template_names()


class SessionCreateView(CreateView):
    model = Session
    form_class = SessionForm
    # fields = ['start', 'end', 'student', 'parent']
    template_name = "students/session_create.html"
    success_url = reverse_lazy("session_list")

    def __init__(self, **kwargs):
        return super(SessionCreateView, self).__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        return super(SessionCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(SessionCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(SessionCreateView, self).post(request, *args, **kwargs)

    def get_form_class(self):
        return super(SessionCreateView, self).get_form_class()

    def get_form(self, form_class=None):
        return super(SessionCreateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(SessionCreateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(SessionCreateView, self).get_initial()

    def form_invalid(self, form):
        return super(SessionCreateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(SessionCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(SessionCreateView, self).get_context_data(**kwargs)
        return ret

    def render_to_response(self, context, **response_kwargs):
        return super(SessionCreateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(SessionCreateView, self).get_template_names()

    def get_success_url(self):
        return reverse("students:session_detail", args=(self.object.pk,))


class SessionUpdateView(UpdateView):
    model = Session
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

    def dispatch(self, *args, **kwargs):
        return super(SessionUpdateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(SessionUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(SessionUpdateView, self).post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(SessionUpdateView, self).get_object(queryset)
        if obj.end is None:
            if obj.start is not None:
                obj.end = timezone.localtime(obj.start).replace(minute=0,hour=18)
        return obj

    def get_queryset(self):
        return super(SessionUpdateView, self).get_queryset()

    def get_slug_field(self):
        return super(SessionUpdateView, self).get_slug_field()

    def get_form_class(self):
        return super(SessionUpdateView, self).get_form_class()

    def get_form(self, form_class=None):
        return super(SessionUpdateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(SessionUpdateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(SessionUpdateView, self).get_initial()

    def form_invalid(self, form):
        return super(SessionUpdateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(SessionUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(SessionUpdateView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(SessionUpdateView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(SessionUpdateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(SessionUpdateView, self).get_template_names()

    def get_success_url(self):
        return reverse("students:session_detail", args=(self.object.pk,))


class SessionDeleteView(DeleteView):
    model = Session
    template_name = "students/session_delete.html"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = "session"

    def __init__(self, **kwargs):
        return super(SessionDeleteView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(SessionDeleteView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        return super(SessionDeleteView, self).post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super(SessionDeleteView, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(SessionDeleteView, self).get_object(queryset)

    def get_queryset(self):
        return super(SessionDeleteView, self).get_queryset()

    def get_slug_field(self):
        return super(SessionDeleteView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(SessionDeleteView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(SessionDeleteView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(SessionDeleteView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(SessionDeleteView, self).get_template_names()

    def get_success_url(self):
        return reverse("students:session_list")


class SessionMultiCreateView(FormView):
    #model = Session
    form_class = MultiSessionForm
    # fields = ['start', 'end', 'student', 'parent']
    template_name = "students/session_create_multiple.html"
    #success_url = reverse_lazy("session_list")

    def __init__(self, **kwargs):
        return super(SessionMultiCreateView, self).__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        return super(SessionMultiCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(SessionMultiCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(SessionMultiCreateView, self).post(request, *args, **kwargs)

    def get_form_class(self):
        return super(SessionMultiCreateView, self).get_form_class()

    def get_form(self, form_class=None):
        return super(SessionMultiCreateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(SessionMultiCreateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(SessionMultiCreateView, self).get_initial()

    def form_invalid(self, form):
        return super(SessionMultiCreateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        #obj.save()
        return super(SessionMultiCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SessionMultiCreateView, self).get_context_data(**kwargs)
        more_context = {'current_time': datetime.today().strftime('%A, %B %d, %Y')}
        context.update(more_context)
        return context

    def render_to_response(self, context, **response_kwargs):
        return super(SessionMultiCreateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(SessionMultiCreateView, self).get_template_names()

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Sessions started')
        return reverse("students:session_create_multiple")
        #return reverse("students:session_detail", args=(self.object.pk,))


class SessionMultiEndView(FormView):
    #model = Session
    form_class = MultiSessionEndForm
    # fields = ['start', 'end', 'student', 'parent']
    template_name = "students/session_end_multiple.html"
    #success_url = reverse_lazy("session_list")

    def __init__(self, **kwargs):
        return super(SessionMultiEndView, self).__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        return super(SessionMultiEndView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(SessionMultiEndView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(SessionMultiEndView, self).post(request, *args, **kwargs)

    def get_form_class(self):
        return super(SessionMultiEndView, self).get_form_class()

    def get_form(self, form_class=None):
        return super(SessionMultiEndView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(SessionMultiEndView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(SessionMultiEndView, self).get_initial()

    def form_invalid(self, form):
        return super(SessionMultiEndView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(SessionMultiEndView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SessionMultiEndView, self).get_context_data(**kwargs)
        more_context = {'current_time': datetime.today().strftime('%A, %B %d, %Y')}
        context.update(more_context)
        return context

    def render_to_response(self, context, **response_kwargs):
        return super(SessionMultiEndView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(SessionMultiEndView, self).get_template_names()

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Session ended')
        return reverse("students:session_end_multiple")
        #return reverse("students:session_detail", args=(self.object.pk,))


class SessionTodayView(ListView):
    model = Session
    template_name = "students/session_today.html"
    paginate_by = 2000
    context_object_name = "session_list"
    allow_empty = True
    page_kwarg = 'page'
    paginate_orphans = 0

    def __init__(self, **kwargs):
        return super(SessionTodayView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(SessionTodayView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(SessionTodayView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        #s = super(SessionListView, self).get_queryset()
        return Session.objects.filter(start__gt=timezone.now().replace(hour=0,minute=1)).order_by('student__grade','student__name')

    def get_allow_empty(self):
        return super(SessionTodayView, self).get_allow_empty()

    def get_context_data(self, *args, **kwargs):
        ret = super(SessionTodayView, self).get_context_data(*args, **kwargs)
        return ret

    def get_paginate_by(self, queryset):
        return super(SessionTodayView, self).get_paginate_by(queryset)

    def get_context_object_name(self, object_list):
        return super(SessionTodayView, self).get_context_object_name(object_list)

    def paginate_queryset(self, queryset, page_size):
        return super(SessionTodayView, self).paginate_queryset(queryset, page_size)

    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True):
        return super(SessionTodayView, self).get_paginator(queryset, per_page, orphans=0, allow_empty_first_page=True)

    def render_to_response(self, context, **response_kwargs):
        return super(SessionTodayView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(SessionTodayView, self).get_template_names()

class WhereIsView(FormView):
    #model = Session
    form_class = WhereIsForm
    # fields = ['start', 'end', 'student', 'parent']
    template_name = "students/where_is.html"
    #success_url = reverse_lazy("session_list")

    def __init__(self, **kwargs):
        return super(WhereIsView, self).__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        return super(WhereIsView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(WhereIsView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(WhereIsView, self).post(request, *args, **kwargs)

    def get_form_class(self):
        return super(WhereIsView, self).get_form_class()

    def get_form(self, form_class=None):
        return super(WhereIsView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(WhereIsView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(WhereIsView, self).get_initial()

    def form_invalid(self, form):
        return super(WhereIsView, self).form_invalid(form)

    def form_valid(self, form, **kwargs):
        obj = form.save(commit=False)
        iterobj = iter(obj)
        
#        if iterobj:
#            o = next(iterobj)
#            m = f"<span class=\"font-weight-italic\">{o.start.strftime('%I:%M %p')}-{o.end.strftime('%I:%M %p')}</span>: {o.course} ({o.teacher}) in <span class=\"font-weight-bold\">{o.room}</span>"
#            messages.success(self.request, m, extra_tags='safe')
#        else:
#            messages.error(self.request,'Unknown')

        for o in iterobj:
            #m = f"{o.start.strftime('%I:%M %p')}-{o.end.strftime('%I:%M %p')}: {o.course} ({o.teacher}) in Room {o.room}"
            m = f"<span class=\"font-weight-italic\">{o.start.strftime('%I:%M %p')}-{o.end.strftime('%I:%M %p')}</span>: {o.course} ({o.teacher}) in <span class=\"font-weight-bold\">{o.room}</span>"
            if o.current:
                messages.success(self.request, m, extra_tags='safe')
            else:
                messages.warning(self.request, m, extra_tags='safe')
            

        return super(WhereIsView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(WhereIsView, self).get_context_data(**kwargs)
        more_context = {'current_time': datetime.today().strftime('%A, %B %d, %Y')}
        context.update(more_context)
        return context

    def render_to_response(self, context, **response_kwargs):
        return super(WhereIsView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(WhereIsView, self).get_template_names()

    def get_success_url(self):
        return reverse("where_is")
        #return reverse("students:session_detail", args=(self.object.pk,))
