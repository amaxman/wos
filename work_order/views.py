from django.contrib.auth.models import User
from django.utils import timezone

from core.views import BasicListView, BasicRetrieveUpdateDestroyAPIView, ListCreateAPIView, PostDataFilterBackend
from .models import WorkOrder, WorkOrderStaff
from .serializers import WorkOrderSerializer, WorkOrderStaffSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext_lazy as _


# region 工单
class WorkOrderListView(BasicListView):
    """
   工单管理视图集

   支持的查询参数:
   - start_time: 按开始日期筛选 (格式: YYYY-MM-DD)
   - start_time__gte: 开始日期大于等于指定日期
   - start_time__lte: 开始日期小于等于指定日期
   - search: 搜索工单标题和内容
   - ordering: 排序字段 (例如: ordering=start_time 或 ordering=-start_time)
   """
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer

    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_backends = [PostDataFilterBackend, DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        'start_time': ['exact', 'gte', 'lte'],
        'title': ['icontains'],
        'content': ['icontains'],
    }
    search_fields = ['title', 'content']
    ordering_fields = ['-start_time', '-end_time', 'create_time']
    ordering = ['-start_time']  # 默认按开始日期降序排列

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

    def post(self, request, *args, **kwargs):
        """
        处理POST请求，返回过滤后的列表数据
        """
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        # 应用过滤和排序
        queryset = self.filter_queryset(self.get_queryset())

        # 应用过滤

        # 手动处理分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # 使用内置的分页响应方法，会自动处理page_size参数
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class WorkOrderListCreateView(ListCreateAPIView):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()  # 复制数据，因为 request.data 是不可变的

        # region 获取用户信息
        # 获取当前用户
        user = request.user
        data['create_by'] = user.id
        data['create_time'] = timezone.now()
        data['update_by'] = user.id
        data['update_time'] = timezone.now()
        # endregion

        # region 开始日期
        start_date = data['start_date']
        end_date = data['end_date']
        if start_date is None:
            return Response({
                'msgType': False,
                'msg': _('Start Date Required'),
            }, status=status.HTTP_201_CREATED)
        # endregion
        # region 开始时间与结束时间比较
        if end_date is not None:
            if start_date > end_date:
                return Response({
                    'msgType': False,
                    'msg': _('Check Date Area'),
                }, status=status.HTTP_201_CREATED)

        # endregion

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


class WorkOrderRetrieveUpdateDestroyView(BasicRetrieveUpdateDestroyAPIView):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer


# endregion

# region 工单项
class WorkOrderStaffListView(BasicListView):
    queryset = WorkOrderStaff.objects.all()
    serializer_class = WorkOrderStaffSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        work_order_id = self.request.query_params.get('work_order_id')
        if work_order_id is not None:
            queryset = queryset.filter(work_order_id=work_order_id)
        return queryset


class WorkOrderStaffListCreateView(ListCreateAPIView):
    queryset = WorkOrderStaff.objects.all()
    serializer_class = WorkOrderStaffSerializer

    def check_staff_exist(self, workOrderId: int, staffId: int) -> bool:
        """检查工单是否已关联指定工作人员（优化版）"""
        return WorkOrderStaff.objects.filter(
            work_order_id=workOrderId,
            staff_id=staffId
        ).exists()

    def create(self, request, *args, **kwargs):
        data = request.data.copy()  # 复制数据，因为 request.data 是不可变的

        # 使用修改后的数据创建序列化器
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # region 获取work_order_id并确定是否存在
        work_order_id = data.get('work_order')
        if work_order_id is None or work_order_id == '':
            return Response({
                'msgType': False,
                'msg': _('Work Order Staff Work Id Required'),
            }, status=status.HTTP_201_CREATED)

        workOrder: WorkOrder = WorkOrder.objects.get(id=work_order_id)
        if workOrder is None:
            return Response({
                'msgType': False,
                'msg': _('Work Order Deleted'),
            }, status=status.HTTP_201_CREATED)
        # endregion

        # region 根据staff_id获取
        staffId: str = data.get('staff')
        if staffId is None or staffId == '':
            return Response({
                'msgType': False,
                'msg': _('Work Order Staff Staff Id Required'),
            }, status=status.HTTP_201_CREATED)
        user: User = User.objects.get(id=staffId)
        if user is None:
            return Response({
                'msgType': False,
                'msg': _('User not found'),
            }, status=status.HTTP_201_CREATED)
        # endregion

        # region 是否执行人已经被添加
        checkStaff = self.check_staff_exist(int(work_order_id), int(staffId))
        if checkStaff:
            return Response({
                'msgType': False,
                'msg': _('Work Order Staff Repeated'),
            }, status=status.HTTP_201_CREATED)
        # endregion

        # region 获取用户信息
        # 获取当前用户
        user = request.user
        data['create_by'] = user.id
        data['create_time'] = timezone.now()
        data['update_by'] = user.id
        data['update_time'] = timezone.now()
        # endregion

        work_order_percent: float = float(data.get('work_order_percent')) / 100
        if work_order_percent is None:
            data['work_order_percent'] = 0
        else:
            if work_order_percent < 0:
                return Response({
                    'msgType': False,
                    'msg': _('Percent Check MinValue'),
                }, status=status.HTTP_201_CREATED)
            elif work_order_percent > 100:
                return Response({
                    'msgType': False,
                    'msg': _('Percent Check MaxValue'),
                }, status=status.HTTP_201_CREATED)

        self.perform_create(serializer)

        # 返回响应
        headers = self.get_success_headers(serializer.data)
        return Response({
            'msgType': True,
            'msg': _('Save Successfully'),
            'data': serializer.data.get('id'),
        }, status=status.HTTP_201_CREATED, headers=headers)


class WorkOrderStaffRetrieveUpdateDestroyView(BasicRetrieveUpdateDestroyAPIView):
    queryset = WorkOrderStaff.objects.all()
    serializer_class = WorkOrderStaffSerializer
# endregion
