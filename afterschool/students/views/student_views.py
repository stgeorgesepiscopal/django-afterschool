from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from ..models import Student
from ..forms import StudentForm
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import Http404


class StudentListView(ListView):
    model = Student
    template_name = "students/student_list.html"
    paginate_by = 500
    context_object_name = "student_list"
    allow_empty = True
    page_kwarg = 'page'
    paginate_orphans = 0

    def __init__(self, **kwargs):
        return super(StudentListView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(StudentListView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(StudentListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return super(StudentListView, self).get_queryset()

    def get_allow_empty(self):
        return super(StudentListView, self).get_allow_empty()

    def get_context_data(self, *args, **kwargs):
        ret = super(StudentListView, self).get_context_data(*args, **kwargs)
        return ret

    def get_paginate_by(self, queryset):
        return super(StudentListView, self).get_paginate_by(queryset)

    def get_context_object_name(self, object_list):
        return super(StudentListView, self).get_context_object_name(object_list)

    def paginate_queryset(self, queryset, page_size):
        return super(StudentListView, self).paginate_queryset(queryset, page_size)

    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True):
        return super(StudentListView, self).get_paginator(queryset, per_page, orphans=0, allow_empty_first_page=True)

    def render_to_response(self, context, **response_kwargs):
        return super(StudentListView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(StudentListView, self).get_template_names()


class StudentDetailView(DetailView):
    model = Student
    template_name = "students/student_detail.html"
    context_object_name = "student"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'

    def __init__(self, **kwargs):
        return super(StudentDetailView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(StudentDetailView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(StudentDetailView, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(StudentDetailView, self).get_object(queryset)

    def get_queryset(self):
        return super(StudentDetailView, self).get_queryset()

    def get_slug_field(self):
        return super(StudentDetailView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(StudentDetailView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(StudentDetailView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(StudentDetailView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(StudentDetailView, self).get_template_names()


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    # fields = ['name', 'grade']
    template_name = "students/student_create.html"
    success_url = reverse_lazy("student_list")

    def __init__(self, **kwargs):
        return super(StudentCreateView, self).__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        return super(StudentCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(StudentCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(StudentCreateView, self).post(request, *args, **kwargs)

    def get_form_class(self):
        return super(StudentCreateView, self).get_form_class()

    def get_form(self, form_class=None):
        return super(StudentCreateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(StudentCreateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(StudentCreateView, self).get_initial()

    def form_invalid(self, form):
        return super(StudentCreateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(StudentCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(StudentCreateView, self).get_context_data(**kwargs)
        return ret

    def render_to_response(self, context, **response_kwargs):
        return super(StudentCreateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(StudentCreateView, self).get_template_names()

    def get_success_url(self):
        return reverse("students:student_detail", args=(self.object.pk,))


class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    # fields = ['name', 'grade']
    template_name = "students/student_update.html"
    initial = {}
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = "student"

    def __init__(self, **kwargs):
        return super(StudentUpdateView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(StudentUpdateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(StudentUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(StudentUpdateView, self).post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(StudentUpdateView, self).get_object(queryset)

    def get_queryset(self):
        return super(StudentUpdateView, self).get_queryset()

    def get_slug_field(self):
        return super(StudentUpdateView, self).get_slug_field()

    def get_form_class(self):
        return super(StudentUpdateView, self).get_form_class()

    def get_form(self, form_class=None):
        return super(StudentUpdateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(StudentUpdateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(StudentUpdateView, self).get_initial()

    def form_invalid(self, form):
        return super(StudentUpdateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(StudentUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(StudentUpdateView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(StudentUpdateView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(StudentUpdateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(StudentUpdateView, self).get_template_names()

    def get_success_url(self):
        return reverse("students:student_detail", args=(self.object.pk,))


class StudentDeleteView(DeleteView):
    model = Student
    template_name = "students/student_delete.html"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = "student"

    def __init__(self, **kwargs):
        return super(StudentDeleteView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(StudentDeleteView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        return super(StudentDeleteView, self).post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super(StudentDeleteView, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(StudentDeleteView, self).get_object(queryset)

    def get_queryset(self):
        return super(StudentDeleteView, self).get_queryset()

    def get_slug_field(self):
        return super(StudentDeleteView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(StudentDeleteView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(StudentDeleteView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(StudentDeleteView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(StudentDeleteView, self).get_template_names()

    def get_success_url(self):
        return reverse("students:student_list")
