from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from ..models import DayofWeek
from ..forms import DayofWeekForm
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import Http404


class DayofWeekListView(ListView):
    model = DayofWeek
    template_name = "students/dayof_week_list.html"
    paginate_by = 20
    context_object_name = "dayof_week_list"
    allow_empty = True
    page_kwarg = 'page'
    paginate_orphans = 0

    def __init__(self, **kwargs):
        return super(DayofWeekListView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(DayofWeekListView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(DayofWeekListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return super(DayofWeekListView, self).get_queryset()

    def get_allow_empty(self):
        return super(DayofWeekListView, self).get_allow_empty()

    def get_context_data(self, *args, **kwargs):
        ret = super(DayofWeekListView, self).get_context_data(*args, **kwargs)
        return ret

    def get_paginate_by(self, queryset):
        return super(DayofWeekListView, self).get_paginate_by(queryset)

    def get_context_object_name(self, object_list):
        return super(DayofWeekListView, self).get_context_object_name(object_list)

    def paginate_queryset(self, queryset, page_size):
        return super(DayofWeekListView, self).paginate_queryset(queryset, page_size)

    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True):
        return super(DayofWeekListView, self).get_paginator(queryset, per_page, orphans=0, allow_empty_first_page=True)

    def render_to_response(self, context, **response_kwargs):
        return super(DayofWeekListView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(DayofWeekListView, self).get_template_names()


class DayofWeekDetailView(DetailView):
    model = DayofWeek
    template_name = "students/dayof_week_detail.html"
    context_object_name = "dayof_week"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'

    def __init__(self, **kwargs):
        return super(DayofWeekDetailView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(DayofWeekDetailView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(DayofWeekDetailView, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(DayofWeekDetailView, self).get_object(queryset)

    def get_queryset(self):
        return super(DayofWeekDetailView, self).get_queryset()

    def get_slug_field(self):
        return super(DayofWeekDetailView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(DayofWeekDetailView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(DayofWeekDetailView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(DayofWeekDetailView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(DayofWeekDetailView, self).get_template_names()


class DayofWeekCreateView(CreateView):
    model = DayofWeek
    form_class = DayofWeekForm
    # fields = ['day']
    template_name = "students/dayof_week_create.html"
    success_url = reverse_lazy("dayof_week_list")

    def __init__(self, **kwargs):
        return super(DayofWeekCreateView, self).__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        return super(DayofWeekCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(DayofWeekCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(DayofWeekCreateView, self).post(request, *args, **kwargs)

    def get_form_class(self):
        return super(DayofWeekCreateView, self).get_form_class()

    def get_form(self, form_class=None):
        return super(DayofWeekCreateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(DayofWeekCreateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(DayofWeekCreateView, self).get_initial()

    def form_invalid(self, form):
        return super(DayofWeekCreateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(DayofWeekCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(DayofWeekCreateView, self).get_context_data(**kwargs)
        return ret

    def render_to_response(self, context, **response_kwargs):
        return super(DayofWeekCreateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(DayofWeekCreateView, self).get_template_names()

    def get_success_url(self):
        return reverse("students:dayof_week_detail", args=(self.object.pk,))


class DayofWeekUpdateView(UpdateView):
    model = DayofWeek
    form_class = DayofWeekForm
    # fields = ['day']
    template_name = "students/dayof_week_update.html"
    initial = {}
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = "dayof_week"

    def __init__(self, **kwargs):
        return super(DayofWeekUpdateView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(DayofWeekUpdateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(DayofWeekUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(DayofWeekUpdateView, self).post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(DayofWeekUpdateView, self).get_object(queryset)

    def get_queryset(self):
        return super(DayofWeekUpdateView, self).get_queryset()

    def get_slug_field(self):
        return super(DayofWeekUpdateView, self).get_slug_field()

    def get_form_class(self):
        return super(DayofWeekUpdateView, self).get_form_class()

    def get_form(self, form_class=None):
        return super(DayofWeekUpdateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(DayofWeekUpdateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(DayofWeekUpdateView, self).get_initial()

    def form_invalid(self, form):
        return super(DayofWeekUpdateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(DayofWeekUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(DayofWeekUpdateView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(DayofWeekUpdateView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(DayofWeekUpdateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(DayofWeekUpdateView, self).get_template_names()

    def get_success_url(self):
        return reverse("students:dayof_week_detail", args=(self.object.pk,))


class DayofWeekDeleteView(DeleteView):
    model = DayofWeek
    template_name = "students/dayof_week_delete.html"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = "dayof_week"

    def __init__(self, **kwargs):
        return super(DayofWeekDeleteView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(DayofWeekDeleteView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        return super(DayofWeekDeleteView, self).post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super(DayofWeekDeleteView, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(DayofWeekDeleteView, self).get_object(queryset)

    def get_queryset(self):
        return super(DayofWeekDeleteView, self).get_queryset()

    def get_slug_field(self):
        return super(DayofWeekDeleteView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(DayofWeekDeleteView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(DayofWeekDeleteView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(DayofWeekDeleteView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(DayofWeekDeleteView, self).get_template_names()

    def get_success_url(self):
        return reverse("students:dayof_week_list")
