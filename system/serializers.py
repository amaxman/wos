from rest_framework import serializers
from .models import DictType, DictData


class DictTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DictType
        fields = ['id', 'dict_name', 'dict_type']
        # fields = '__all__'


class DictDataSerializer(serializers.ModelSerializer):
    # 嵌套显示 DictType 信息，而不仅显示外键 ID
    dict_type = serializers.StringRelatedField(read_only=True)
    dict_type_id = serializers.PrimaryKeyRelatedField(
        queryset=DictType.objects.all(),
        source='dict_type',
        write_only=True
    )

    class Meta:
        model = DictData
        # fields = ['id', 'dict_label', 'dict_value', 'dict_order_num']
        fields = '__all__'
