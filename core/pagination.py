# pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from core.rest_util import JsonMsg
from rest_framework.pagination import LimitOffsetPagination
from django.utils.translation import gettext_lazy as _


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10  # 默认每页显示10条
    max_limit = 100  # 最大允许的limit值
    limit_query_param = 'limit'  # 查询参数名：limit
    offset_query_param = 'offset'  # 查询参数名：offset

    def get_limit(self, request):
        """优先从 POST 数据获取 limit 参数"""
        if request.method == 'POST' and 'limit' in request.data:
            try:
                return int(request.data['limit'])
            except (ValueError, TypeError):
                pass
        return super().get_limit(request)

    def get_offset(self, request):
        """优先从 POST 数据获取 offset 参数"""
        if request.method == 'POST' and 'offset' in request.data:
            try:
                return int(request.data['offset'])
            except (ValueError, TypeError):
                pass
        return super().get_offset(request)

    def get_paginated_response(self, data):
        response_data = {
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.count,
            'limit': self.limit,
            'offset': self.offset,
            'list': data
        }
        jsonMsg: JsonMsg = JsonMsg(msgType=True, msg=_('Paging Successfully'), data=response_data)
        return Response(jsonMsg.to_dict())
