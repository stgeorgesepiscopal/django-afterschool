from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from ..models import Family
from ..forms import FamilyForm
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import Http404


class FamilyListView(ListView):
    model = Family
    template_name = "students/family_list.html"
    paginate_by = 20
    context_object_name = "family_list"
    allow_empty = True
    page_kwarg = 'page'
    paginate_orphans = 0

    def __init__(self, **kwargs):
        return super(FamilyListView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(FamilyListView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(FamilyListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return super(FamilyListView, self).get_queryset()

    def get_allow_empty(self):
        return super(FamilyListView, self).get_allow_empty()

    def get_context_data(self, *args, **kwargs):
        ret = super(FamilyListView, self).get_context_data(*args, **kwargs)
        return ret

    def get_paginate_by(self, queryset):
        return super(FamilyListView, self).get_paginate_by(queryset)

    def get_context_object_name(self, object_list):
        return super(FamilyListView, self).get_context_object_name(object_list)

    def paginate_queryset(self, queryset, page_size):
        return super(FamilyListView, self).paginate_queryset(queryset, page_size)

    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True):
        return super(FamilyListView, self).get_paginator(queryset, per_page, orphans=0, allow_empty_first_page=True)

    def render_to_response(self, context, **response_kwargs):
        return super(FamilyListView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(FamilyListView, self).get_template_names()


class FamilyDetailView(DetailView):
    model = Family
    template_name = "students/family_detail.html"
    context_object_name = "family"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'

    def __init__(self, **kwargs):
        return super(FamilyDetailView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(FamilyDetailView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(FamilyDetailView, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(FamilyDetailView, self).get_object(queryset)

    def get_queryset(self):
        return super(FamilyDetailView, self).get_queryset()

    def get_slug_field(self):
        return super(FamilyDetailView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(FamilyDetailView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(FamilyDetailView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(FamilyDetailView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(FamilyDetailView, self).get_template_names()


class FamilyCreateView(CreateView):
    model = Family
    form_class = FamilyForm
    # fields = ['name']
    template_name = "students/family_create.html"
    success_url = reverse_lazy("family_list")

    def __init__(self, **kwargs):
        return super(FamilyCreateView, self).__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        return super(FamilyCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(FamilyCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(FamilyCreateView, self).post(request, *args, **kwargs)

    def get_form_class(self):
        return super(FamilyCreateView, self).get_form_class()

    def get_form(self, form_class=None):
        return super(FamilyCreateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(FamilyCreateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(FamilyCreateView, self).get_initial()

    def form_invalid(self, form):
        return super(FamilyCreateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(FamilyCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(FamilyCreateView, self).get_context_data(**kwargs)
        return ret

    def render_to_response(self, context, **response_kwargs):
        return super(FamilyCreateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(FamilyCreateView, self).get_template_names()

    def get_success_url(self):
        return reverse("students:family_detail", args=(self.object.pk,))


class FamilyUpdateView(UpdateView):
    model = Family
    form_class = FamilyForm
    # fields = ['name']
    template_name = "students/family_update.html"
    initial = {}
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = "family"

    def __init__(self, **kwargs):
        return super(FamilyUpdateView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(FamilyUpdateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(FamilyUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(FamilyUpdateView, self).post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(FamilyUpdateView, self).get_object(queryset)

    def get_queryset(self):
        return super(FamilyUpdateView, self).get_queryset()

    def get_slug_field(self):
        return super(FamilyUpdateView, self).get_slug_field()

    def get_form_class(self):
        return super(FamilyUpdateView, self).get_form_class()

    def get_form(self, form_class=None):
        return super(FamilyUpdateView, self).get_form(form_class)

    def get_form_kwargs(self, **kwargs):
        return super(FamilyUpdateView, self).get_form_kwargs(**kwargs)

    def get_initial(self):
        return super(FamilyUpdateView, self).get_initial()

    def form_invalid(self, form):
        return super(FamilyUpdateView, self).form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super(FamilyUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(FamilyUpdateView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(FamilyUpdateView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(FamilyUpdateView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(FamilyUpdateView, self).get_template_names()

    def get_success_url(self):
        return reverse("students:family_detail", args=(self.object.pk,))


class FamilyDeleteView(DeleteView):
    model = Family
    template_name = "students/family_delete.html"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    context_object_name = "family"

    def __init__(self, **kwargs):
        return super(FamilyDeleteView, self).__init__(**kwargs)

    def dispatch(self, *args, **kwargs):
        return super(FamilyDeleteView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        return super(FamilyDeleteView, self).post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super(FamilyDeleteView, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super(FamilyDeleteView, self).get_object(queryset)

    def get_queryset(self):
        return super(FamilyDeleteView, self).get_queryset()

    def get_slug_field(self):
        return super(FamilyDeleteView, self).get_slug_field()

    def get_context_data(self, **kwargs):
        ret = super(FamilyDeleteView, self).get_context_data(**kwargs)
        return ret

    def get_context_object_name(self, obj):
        return super(FamilyDeleteView, self).get_context_object_name(obj)

    def render_to_response(self, context, **response_kwargs):
        return super(FamilyDeleteView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        return super(FamilyDeleteView, self).get_template_names()

    def get_success_url(self):
        return reverse("students:family_list")
