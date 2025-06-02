from django.contrib import admin

from system.ModelAdmins import DictTypeAdmin, DictDataAdmin, MobileAccessAdmin
from system.models import DictType, DictData, MobileAccess

admin.site.register(DictType, DictTypeAdmin)
admin.site.register(DictData, DictDataAdmin)
admin.site.register(MobileAccess, MobileAccessAdmin)
