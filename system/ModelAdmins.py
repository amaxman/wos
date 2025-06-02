from django.contrib import admin
from django.utils.html import format_html


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
                '<a href="/{}" target="_blank" title="点击查看原图"><img src="/{}" class="mobile_access_image" /></a>',
                obj.access_icon,
                obj.access_icon
            )
        return "无图片"

    image_display.short_description = '图片'  # 设置列标题
    image_display.admin_order_field = 'access_icon'

    def image_preview(self, obj):
        """在详情页显示图片预览"""
        if obj.access_icon:
            return format_html(
                '<img src="/{}" class="mobile_access_image" />',
                obj.access_icon
            )
        return "无图片"
    image_preview.short_description = '图片预览'

    class Media:
        css = {
            'all': ('css/custom.css',)
        }
