from rest_framework import serializers

from core.serializer import ModelsSerializer
from system.models import DictType, DictData
from users.serializers import UserInfoSerializer
from .models import WorkOrder, WorkOrderStaff

from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class WorkOrderSerializer(ModelsSerializer):
    # 嵌套显示 DictType 信息，而不仅显示外键 ID
    # cate = serializers.StringRelatedField(read_only=False)
    cate = serializers.PrimaryKeyRelatedField(
        label=_('Work Order Cate'),
        queryset=DictData.objects.filter(dict_type__dict_type='work_order_cate'),
        write_only=False
    )
    # level = serializers.StringRelatedField(read_only=False)
    level = serializers.PrimaryKeyRelatedField(
        label=_('Work Order Level'),
        queryset=DictData.objects.filter(dict_type__dict_type='work_order_level'),
        write_only=False
    )

    class Meta:
        model = WorkOrder
        fields = ['id', 'title', 'content', 'start_time', 'end_time', 'cate', 'level',
                  'create_by', 'create_time', 'update_by',
                  'update_time']


class WorkOrderStaffSerializer(ModelsSerializer):
    work_order_title = serializers.CharField(source='work_order.title', read_only=True)
    staff_info = UserInfoSerializer(source='staff', read_only=True)
    staff_first_name = serializers.CharField(source='staff.first_name', read_only=True)
    work_order_percent = serializers.IntegerField(
        label=_('Work Order Staff Percent'),
        validators=[
            MinValueValidator(0, message=_('Percent Check MinValue')),
            MaxValueValidator(100, message=_('Percent Check MaxValue'))
        ]
    )

    class Meta:
        model = WorkOrderStaff
        fields = [
            'id', 'work_order', 'work_order_title', 'staff', 'work_order_percent', 'staff_info', 'staff_first_name',
            'create_by',
            'create_time', 'update_by', 'update_time'
        ]
        read_only_fields = ['create_by', 'create_time', 'update_by', 'update_time']
