from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'email',
        'phone',
        'specialization',
        'experience_years',
        'created_by',
        'created_at',
    )
    search_fields = (
        'name',
        'email',
        'specialization',
        'created_by__email',
        'created_by__username',
    )
    list_filter = ('specialization', 'created_at')
