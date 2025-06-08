from rest_framework import serializers

from core.serializer import ModelsSerializer
from system.models import DictType, DictData
from users.serializers import UserInfoSerializer
from .models import WorkOrder, WorkOrderStaff

from django.utils.translation import gettext_lazy as _


class WorkOrderSerializer(ModelsSerializer):
    # 嵌套显示 DictType 信息，而不仅显示外键 ID
    cate = serializers.StringRelatedField(read_only=True)
    cate_id = serializers.PrimaryKeyRelatedField(
        label=_('Work Order Cate'),
        queryset=DictData.objects.filter(dict_type__dict_type='work_order_cate'),
        source='dict_type',
        write_only=True
    )
    level = serializers.StringRelatedField(read_only=True)
    level_id = serializers.PrimaryKeyRelatedField(
        label=_('Work Order Level'),
        queryset=DictData.objects.filter(dict_type__dict_type='work_order_level'),
        source='dict_type',
        write_only=True
    )

    class Meta:
        model = WorkOrder
        fields = ['id', 'title', 'content', 'start_date', 'end_date', 'cate', 'cate_id', 'level', 'level_id',
                  'create_by', 'create_time', 'update_by',
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
