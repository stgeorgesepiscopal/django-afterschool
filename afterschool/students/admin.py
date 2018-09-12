from django.contrib import admin
from .models import DayofWeek, Student, Family, StudentSession
from django_baker.admin import ExtendedModelAdminMixin


class DayofWeekAdmin(ExtendedModelAdminMixin, admin.ModelAdmin):
    extra_list_display = []
    extra_list_filter = []
    extra_search_fields = []
    list_editable = []
    raw_id_fields = []
    inlines = []
    filter_vertical = []
    filter_horizontal = []
    radio_fields = {}
    prepopulated_fields = {}
    formfield_overrides = {}
    readonly_fields = []


class StudentAdmin(ExtendedModelAdminMixin, admin.ModelAdmin):
    extra_list_display = []
    extra_list_filter = []
    extra_search_fields = []
    list_editable = []
    raw_id_fields = []
    inlines = []
    filter_vertical = []
    filter_horizontal = []
    radio_fields = {}
    prepopulated_fields = {}
    formfield_overrides = {}
    readonly_fields = []


class FamilyAdmin(ExtendedModelAdminMixin, admin.ModelAdmin):
    extra_list_display = []
    extra_list_filter = []
    extra_search_fields = []
    list_editable = []
    raw_id_fields = []
    inlines = []
    filter_vertical = []
    filter_horizontal = []
    radio_fields = {}
    prepopulated_fields = {}
    formfield_overrides = {}
    readonly_fields = []


# class SessionAdmin(ExtendedModelAdminMixin, admin.ModelAdmin):
#    extra_list_display = []
#    extra_list_filter = []
#    extra_search_fields = []
#    list_editable = []
#    raw_id_fields = []
#    inlines = []
#    filter_vertical = []
#    filter_horizontal = []
#    radio_fields = {}
#    prepopulated_fields = {}
#    formfield_overrides = {}
#    readonly_fields = []
class SessionAdmin(admin.ModelAdmin):
    readonly_fields = []


admin.site.register(DayofWeek, DayofWeekAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Family, FamilyAdmin)
admin.site.register(StudentSession, SessionAdmin)
