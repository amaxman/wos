from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


class DictTypeAdmin(admin.ModelAdmin):
    fieldsets = [
        (_('Basic Info'), {
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
        (_('Dict Type'), {
            'fields': [
                'dict_type',
            ],
        }),
        (_('Detail'), {
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
        (_('Basic Info'), {
            'fields': [
                'access_title',
                'access_code',
                'access_order_num',
            ],
        }),
        (_('ICON'), {
            'fields': [
                'access_icon',
                'image_preview'
            ],
        }),
    ]
    list_display = [
        'access_title',
        'image_display',
        'access_code',
        'access_order_num',
    ]
    search_fields = [
        'access_title',
        'access_code',
    ]

    readonly_fields = ('image_preview',)  # 添加图片预览字段

    def image_display(self, obj):
        if obj.access_icon:
            return format_html(
                '<a href="/{}" target="_blank" title="{}"><img src="/{}" class="mobile_access_image" /></a>',
                obj.access_icon,
                _('Click to View Image'),
                obj.access_icon
            )
        return _('No Image')

    image_display.short_description = _('ICON')  # 设置列标题
    image_display.admin_order_field = 'access_icon'

    def image_preview(self, obj):
        """在详情页显示图片预览"""
        if obj.access_icon:
            return format_html(
                '<img src="/{}" class="mobile_access_image" />',
                obj.access_icon
            )
        return _('No Image')
    image_preview.short_description = _('Preview')

    class Media:
        css = {
            'all': ('css/custom.css',)
        }
