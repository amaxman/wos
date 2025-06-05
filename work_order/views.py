from core.views import BasicListView
from .models import WorkOrder, WorkOrderStaff
from .serializers import WorkOrderSerializer, WorkOrderStaffSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status


class WorkOrderListView(BasicListView):
    """
   工单管理视图集

   支持的查询参数:
   - start_date: 按开始日期筛选 (格式: YYYY-MM-DD)
   - start_date__gte: 开始日期大于等于指定日期
   - start_date__lte: 开始日期小于等于指定日期
   - search: 搜索工单标题和内容
   - ordering: 排序字段 (例如: ordering=start_date 或 ordering=-start_date)
   """
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        'start_date': ['exact', 'gte', 'lte'],
    }
    search_fields = ['title', 'content']
    ordering_fields = ['start_date', 'end_date', 'create_time']
    ordering = ['-start_date']  # 默认按开始日期降序排列

    def create(self, request, *args, **kwargs):
        # 自动设置创建人和更新人
        data = request.data.copy()
        if request.user.is_authenticated and 'create_by' not in data:
            data['create_by'] = request.user.id
        if request.user.is_authenticated and 'update_by' not in data:
            data['update_by'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        # 自动设置更新人
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        if request.user.is_authenticated and 'update_by' not in data:
            data['update_by'] = request.user.id
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # 手动处理分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # 使用内置的分页响应方法，会自动处理page_size参数
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def _list(self, request, *args, **kwargs):
        print("===== 进入 list 方法 =====")
        print("请求方法:", request.method)
        print("查询集长度:", self.queryset.count())
        return super().list(request, *args, **kwargs)


class WorkOrderStaffListView(BasicListView):
    queryset = WorkOrderStaff.objects.all()
    serializer_class = WorkOrderStaffSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        work_order_id = self.request.query_params.get('work_order_id')
        if work_order_id is not None:
            queryset = queryset.filter(work_order_id=work_order_id)
        return queryset

    def list(self, request, *args, **kwargs):
        print("===== 进入 list 方法 =====")
        print("请求方法:", request.method)
        print("查询集长度:", self.queryset.count())
        return super().list(request, *args, **kwargs)
