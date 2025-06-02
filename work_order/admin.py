from django.contrib import admin

from work_order.models import WorkOrder, WorkOrderStaff
from work_order.ModelAdmins import WorkOrderAdmin, WorkOrderStaffAdmin

admin.site.register(WorkOrder, WorkOrderAdmin)
admin.site.register(WorkOrderStaff, WorkOrderStaffAdmin)
