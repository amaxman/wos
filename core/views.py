from rest_framework.filters import BaseFilterBackend
from rest_framework.generics import ListAPIView
from .pagination import CustomLimitOffsetPagination
from rest_framework import permissions, generics, status
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from django.db import models

from .rest_util import JsonMsg


class BasicListView(ListAPIView):
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomLimitOffsetPagination


class ListCreateAPIView(generics.ListCreateAPIView):
    def create(self, request, *args, **kwargs):
        data = request.data

        # 使用修改后的数据创建序列化器
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        # 返回响应
        headers = self.get_success_headers(serializer.data)
        return Response({
            'msgType': True,
            'msg': _('Save Successfully'),
            'data': serializer.data.get('id'),
        }, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        """
        处理POST请求，返回过滤后的列表数据
        """
        return self.list(request, *args, **kwargs)


class BasicRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'

    # region 创建数据
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # 返回自定义格式（包含消息和数据）
        return Response({
            'msgType': True,
            'message': _('Dict Type Save Successful'),
            'data': serializer.data.get('id'),
        }, status=status.HTTP_201_CREATED, headers=headers)

    # endregion

    # region 删除数据
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            'msgType': True,
            'msg': _('Delete Successfully'),
        }, status=status.HTTP_204_NO_CONTENT)

    # endregion

    # region 获取单条数据
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # 返回自定义格式（包含消息和数据）
        jsonMsg: JsonMsg = JsonMsg(msgType=True, msg=_('Load Successfully'), data=serializer.data)
        return Response(jsonMsg.to_dict(), status=status.HTTP_200_OK)
    # endregion


class PostDataFilterBackend(BaseFilterBackend):
    """自定义过滤器后端，支持从POST请求体中获取过滤条件"""

    def filter_queryset(self, request, queryset, view):
        # 如果是POST请求，从request.data获取过滤条件
        if request.method == 'POST':
            filters = {}
            for field, lookups in view.filterset_fields.items():
                for lookup in lookups:
                    key = f"{field}__{lookup}" if lookup != 'exact' else field
                    if key in request.data:
                        filters[key] = request.data[key]

            # 处理search字段
            if hasattr(view, 'search_fields') and 'search' in request.data:
                search_term = request.data['search']
                if search_term:
                    # 简单实现：将搜索词应用到所有搜索字段
                    or_queries = []
                    for field in view.search_fields:
                        or_queries.append(models.Q(**{f"{field}__icontains": search_term}))

                    if or_queries:
                        query = or_queries.pop()
                        for q in or_queries:
                            query |= q
                        queryset = queryset.filter(query)

            # 处理排序
            if hasattr(view, 'ordering_fields') and 'ordering' in request.data:
                ordering = request.data['ordering']
                if isinstance(ordering, str):
                    ordering = [ordering]
                # 验证排序字段是否在允许的范围内
                valid_ordering = []
                for field in ordering:
                    field_name = field.lstrip('-')
                    if field_name in view.ordering_fields:
                        valid_ordering.append(field)
                if valid_ordering:
                    queryset = queryset.order_by(*valid_ordering)

            # 应用其他过滤条件
            if filters:
                queryset = queryset.filter(**filters)

            return queryset

        # 对于GET请求，使用默认的过滤逻辑
        return queryset
