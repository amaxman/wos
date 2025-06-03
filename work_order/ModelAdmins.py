from django.contrib import admin
from django.utils.html import format_html

from model.models import BasicModelAdmin
from django.utils.translation import gettext_lazy as _


class WorkOrderAdmin(BasicModelAdmin):
    fieldsets = [
        (_('Basic Info'), {
            'fields': [
                'title',
                'content',
                'cate',
                'level',
            ],
        }),
        (_('Time'), {
            'fields': [
                'start_date',
                'end_date',
            ],
        }),
        (_('User Info'), {
            'fields': [
                'create_by',
                'create_time',
                'update_by',
                'update_time',
            ],
            'classes': ('collapse',),
        }),
    ]
    list_display = [
        'title',
        'content',
        'start_date',
        'end_date',
        'cate',
        'level',
    ]
    search_fields = [
        'title',
        'content',
    ]


class WorkOrderStaffAdmin(BasicModelAdmin):
    fieldsets = [
        (_('Basic Info'), {
            'fields': [
                'work_order',
                'staff_id',
                'work_order_percent',
            ],
        }),
        (_('User Info'), {
            'fields': [
                'create_by',
                'create_time',
                'update_by',
                'update_time',
            ],
            'classes': ('collapse',),
        }),
    ]
    list_display = [
        'work_order',
        'staff_id',
        'work_order_percent',
    ]
