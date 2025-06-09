from rest_framework import serializers
from .models import DictType, DictData, MobileAccess, MobileAccessUser

from django.utils.translation import gettext_lazy as _


class DictTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DictType
        fields = ['id', 'dict_name', 'dict_type']
        # fields = '__all__'


class DictDataSerializer(serializers.ModelSerializer):
    # 嵌套显示 DictType 信息，而不仅显示外键 ID
    dict_type = serializers.StringRelatedField(read_only=True)
    dict_type_id = serializers.PrimaryKeyRelatedField(
        label=_('Dict Type'),
        queryset=DictType.objects,
        source='dict_type',
        write_only=True
    )

    class Meta:
        model = DictData
        fields = ['id', 'dict_label', 'dict_value', 'dict_order_num', 'dict_type_id', 'dict_type']
        # fields = '__all__'


# region 移动端

class MobileAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileAccess
        fields = ['access_title', 'access_code', 'access_order_num', 'access_icon']  # 只包含需要的字段


class MobileAccessUserSerializer(serializers.ModelSerializer):
    # 嵌套序列化关联对象
    mobile_access = MobileAccessSerializer(read_only=True)

    class Meta:
        model = MobileAccessUser
        fields = ['id', 'mobile_access']
# endregion
