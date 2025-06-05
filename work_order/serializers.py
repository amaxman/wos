from rest_framework import serializers

from core.serializer import ModelsSerializer
from users.serializers import UserInfoSerializer
from .models import WorkOrder, WorkOrderStaff


class WorkOrderSerializer(ModelsSerializer):
    class Meta:
        model = WorkOrder
        fields = ['id', 'title', 'content', 'start_date', 'end_date', 'create_by', 'create_time', 'update_by',
                  'update_time']


class WorkOrderStaffSerializer(ModelsSerializer):
    work_order_title = serializers.CharField(source='work_order.title', read_only=True)
    staff_info = UserInfoSerializer(source='staff_id', read_only=True)
    staff_first_name = serializers.CharField(source='staff_id.first_name', read_only=True)

    class Meta:
        model = WorkOrderStaff
        fields = [
            'id', 'work_order', 'work_order_title', 'staff_id',
            'staff_info', 'staff_first_name', 'create_by', 'create_time', 'update_by', 'update_time'
        ]
        read_only_fields = ['create_by', 'create_time', 'update_by', 'update_time']
