from rest_framework.generics import ListAPIView
from .pagination import CustomLimitOffsetPagination
from rest_framework import permissions


class BasicListView(ListAPIView):
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomLimitOffsetPagination
