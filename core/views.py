from rest_framework.generics import ListAPIView
from .pagination import CustomLimitOffsetPagination
from rest_framework import permissions, generics, status
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response

from .rest_util import JsonMsg


class BasicListView(ListAPIView):
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomLimitOffsetPagination


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
