from django.shortcuts import render

from rest_framework import viewsets, permissions, filters
from .models import DictType, DictData
from .serializers import DictTypeSerializer, DictDataSerializer


class DictTypeViewSet(viewsets.ModelViewSet):
    queryset = DictType.objects.all()
    serializer_class = DictTypeSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        print("===== 进入 list 方法 =====")
        print("请求方法:", request.method)
        print("查询集长度:", self.queryset.count())
        return super().list(request, *args, **kwargs)


class DictDataViewSet(viewsets.ModelViewSet):
    """
    API 端点，允许 DictData 实例进行查看和编辑。
    支持按 dict_type 过滤。
    """
    queryset = DictData.objects.all().order_by('dict_order_num')
    serializer_class = DictDataSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['dict_label', 'dict_value']
    ordering_fields = ['dict_order_num', 'dict_label']

    # 支持通过 URL 参数 ?dict_type_id=1 过滤数据
    def get_queryset(self):
        queryset = super().get_queryset()
        dict_type_id = self.request.query_params.get('dict_type_id')
        if dict_type_id is not None:
            queryset = queryset.filter(dict_type_id=dict_type_id)
        return queryset

    def list(self, request, *args, **kwargs):
        print("===== 进入 list 方法 =====")
        print("请求方法:", request.method)
        print("查询集长度:", self.queryset.count())
        return super().list(request, *args, **kwargs)
