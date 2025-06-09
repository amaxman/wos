from django.contrib import admin

from system.ModelAdmins import DictTypeAdmin, DictDataAdmin, MobileAccessAdmin, MobileAccessUserAdmin
from system.models import DictType, DictData, MobileAccess, MobileAccessUser

admin.site.register(DictType, DictTypeAdmin)
admin.site.register(DictData, DictDataAdmin)
admin.site.register(MobileAccess, MobileAccessAdmin)
admin.site.register(MobileAccessUser, MobileAccessUserAdmin)
