from django.contrib import admin
from django.utils.html import format_html

from model.models import BasicModelAdmin


class WorkOrderAdmin(BasicModelAdmin):
    fieldsets = [
        ('基础信息', {
            'fields': [
                'title',
                'content',
            ],
        }),
        ('时间', {
            'fields': [
                'start_date',
                'end_date',
            ],
        }),
        ('用户信息', {
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
    ]
    search_fields = [
        'title',
        'content',
    ]


class WorkOrderStaffAdmin(BasicModelAdmin):
    fieldsets = [
        ('基础信息', {
            'fields': [
                'work_order',
                'staff_id',
                'work_order_percent',
            ],
        }),
        ('用户信息', {
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
