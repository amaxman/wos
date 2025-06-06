from rest_framework import filters

from core.views import BasicListView, BasicRetrieveUpdateDestroyAPIView
from .models import DictType, DictData

from .serializers import DictTypeSerializer, DictDataSerializer
from rest_framework.response import Response
from rest_framework import generics, status
from django.utils.translation import gettext_lazy as _


# region 字典类型
class DictTypeListView(BasicListView):
    queryset = DictType.objects.all()
    serializer_class = DictTypeSerializer


class DictTypeListCreateView(generics.ListCreateAPIView):
    queryset = DictType.objects.all()
    serializer_class = DictTypeSerializer


class DictTypeRetrieveUpdateDestroyView(BasicRetrieveUpdateDestroyAPIView):
    queryset = DictType.objects.all()
    serializer_class = DictTypeSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # region 校验编码是否重复
        id: int = instance.id
        dict_type: str = instance.dict_type
        if dict_type is not None and dict_type != '':
            querySet = DictType.objects.exclude(id=id).filter(dict_type__iexact=dict_type).all()
            if querySet.count() > 0:
                return Response({
                    'msgType': False,
                    'msg': _('Save Unsuccessfully'),
                }, status=status.HTTP_200_OK)
        # endregion

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # 如果存在预取数据，需要重建缓存
            instance._prefetched_objects_cache = {}

        return Response({
            'msgType': True,
            'msg': _('Save Successfully'),
            'data': serializer.data.get('id'),
        }, status=status.HTTP_200_OK)


# endregion

# region 自定明细
class DictDataListView(BasicListView):
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


class DictDataListCreateView(generics.ListCreateAPIView):
    queryset = DictData.objects.all()
    serializer_class = DictDataSerializer


class DictDataRetrieveUpdateDestroyView(BasicRetrieveUpdateDestroyAPIView):
    queryset = DictData.objects.all()
    serializer_class = DictDataSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # region 校验编码是否重复
        dict_type_id: int = instance.dict_type_id
        if dict_type_id is not None:
            querySet = DictType.objects.filter(id=dict_type_id)
            if querySet.count() == 0:
                return Response({
                    'msgType': False,
                    'msg': _('Save Unsuccessfully'),
                }, status=status.HTTP_200_OK)
        # endregion

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # 如果存在预取数据，需要重建缓存
            instance._prefetched_objects_cache = {}

        return Response({
            'msgType': True,
            'msg': _('Save Successfully'),
            'data': serializer.data.get('id'),
        }, status=status.HTTP_200_OK)

# endregion
