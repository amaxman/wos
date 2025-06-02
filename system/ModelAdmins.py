from django.contrib import admin


class DictTypeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('基础信息', {
            'fields': [
                'dict_name',
                'dict_type',
                'is_sys',
                'status',
            ],
        }),
    ]
    list_display = [
        'dict_name',
        'dict_type',
    ]
    search_fields = [
        'dict_name',
        'dict_type',
    ]


class DictDataAdmin(admin.ModelAdmin):
    fieldsets = [
        ('字典类型', {
            'fields': [
                'dict_type',
            ],
        }),
        ('明细', {
            'fields': [
                'dict_label',
                'dict_value',
                'dict_order_num',
                'is_sys',
                'status',
            ],
        }),
    ]
    list_display = [
        'dict_type',
        'dict_label',
        'dict_value',
        'dict_order_num',
    ]
    search_fields = [
        'dict_label',
        'dict_value',
    ]


class MobileAccessAdmin(admin.ModelAdmin):
    fieldsets = [
        ('基础信息', {
            'fields': [
                'access_title',
                'access_code',
                'access_order_num',
            ],
        }),
        ('图标', {
            'fields': [
                'access_icon',
            ],
        }),
    ]
    list_display = [
        'access_icon',
        'access_title',
        'access_code',
        'access_order_num',
    ]
    search_fields = [
        'access_title',
        'access_code',
    ]
