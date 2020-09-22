from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from ..models import Staff
from ..forms import StaffForm
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import Http404

import csv


class StaffListView(ListView):
    model = Staff
    template_name = "students/staff_list.html"
    paginate_by = 500
    context_object_name = "staff_list"
    allow_empty = True
    page_kwarg = 'page'
    paginate_orphans = 0
    ordering = ['name']

    def __init__(self, **kwargs):
        return super(StaffListView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(StaffListView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(StaffListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return super(StaffListView, self).get_queryset()

    def get_allow_empty(self):
        return super(StaffListView, self).get_allow_empty()

    def get_context_data(self, *args, **kwargs):
        ret = super(StaffListView, self).get_context_data(*args, **kwargs)
        return ret

    def get_paginate_by(self, queryset):
        return super(StaffListView, self).get_paginate_by(queryset)

    def get_context_object_name(self, object_list):
        return super(StaffListView, self).get_context_object_name(object_list)

    def paginate_queryset(self, queryset, page_size):
        return super(StaffListView, self).paginate_queryset(queryset, page_size)

    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True):
        return super(StaffListView, self).get_paginator(queryset, per_page, orphans=0, allow_empty_first_page=True)

    def render_to_response(self, context, **response_kwargs):
        return super(StaffListView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(StaffListView, self).get_template_names()


class StaffDetailView(DetailView):
    model = Staff
    template_name = "students/staff_detail.html"
    context_object_name = "staff"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'

    def __init__(self, **kwargs):
        return super(StaffDetailView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(StaffDetailView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(StaffDetailView, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(StaffDetailView, self).get_object(queryset)

    def get_queryset(self):
        return super(StaffDetailView, self).get_queryset()

    def get_slug_field(self):
        return super(StaffDetailView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(StaffDetailView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(StaffDetailView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(StaffDetailView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(StaffDetailView, self).get_template_names()


class StaffCreateView(CreateView):
    model = Staff
    form_class = StaffForm
    # fields = ['name', 'grade']
    template_name = "students/staff_create.html"
    success_url = reverse_lazy("staff_list")

    def __init__(self, **kwargs):
        return super(StaffCreateView, self).__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        return super(StaffCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(StaffCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(StaffCreateView, self).post(request, *args, **kwargs)

    def get_form_class(self):
        return super(StaffCreateView, self).get_form_class()

    def get_form(self, form_class=None):
        return super(StaffCreateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(StaffCreateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(StaffCreateView, self).get_initial()

    def form_invalid(self, form):
        return super(StaffCreateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(StaffCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(StaffCreateView, self).get_context_data(**kwargs)
        return ret

    def render_to_response(self, context, **response_kwargs):
        return super(StaffCreateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(StaffCreateView, self).get_template_names()

    def get_success_url(self):
        #return reverse("students:student_detail", args=(self.object.pk,))
        return reverse("students:staff_list")


class StaffUpdateView(UpdateView):
    model = Staff
    form_class = StaffForm
    # fields = ['name', 'grade']
    template_name = "students/staff_update.html"
    initial = {}
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = "staff"

    def __init__(self, **kwargs):
        return super(StaffUpdateView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(StaffUpdateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(StaffUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(StaffUpdateView, self).post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(StaffUpdateView, self).get_object(queryset)

    def get_queryset(self):
        return super(StaffUpdateView, self).get_queryset()

    def get_slug_field(self):
        return super(StaffUpdateView, self).get_slug_field()

    def get_form_class(self):
        return super(StaffUpdateView, self).get_form_class()

    def get_form(self, form_class=None):
        return super(StaffUpdateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(StaffUpdateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(StaffUpdateView, self).get_initial()

    def form_invalid(self, form):
        return super(StaffUpdateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(StaffUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(StaffUpdateView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(StaffUpdateView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(StaffUpdateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(StaffUpdateView, self).get_template_names()

    def get_success_url(self):
        #return reverse("students:student_detail", args=(self.object.pk,))
        return reverse("students:staff_list")


class StaffDeleteView(DeleteView):
    model = Staff
    template_name = "students/staff_delete.html"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = "staff"

    def __init__(self, **kwargs):
        return super(StaffDeleteView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(StaffDeleteView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        return super(StaffDeleteView, self).post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super(StaffDeleteView, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(StaffDeleteView, self).get_object(queryset)

    def get_queryset(self):
        return super(StaffDeleteView, self).get_queryset()

    def get_slug_field(self):
        return super(StaffDeleteView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(StaffDeleteView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(StaffDeleteView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(StaffDeleteView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(StaffDeleteView, self).get_template_names()

    def get_success_url(self):
        return reverse("students:staff_list")

