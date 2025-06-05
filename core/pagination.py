# pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from core.rest_util import JsonMsg
from rest_framework.pagination import LimitOffsetPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10  # 默认每页显示10条
    max_limit = 100  # 最大允许的limit值
    limit_query_param = 'limit'  # 查询参数名：limit
    offset_query_param = 'offset'  # 查询参数名：offset

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.count,
            'limit': self.limit,
            'offset': self.offset,
            'results': data
        })
