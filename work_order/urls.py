from django.urls import path
from .views import WorkOrderListView, WorkOrderStaffListView

# API URL 现在由路由器自动确定
urlpatterns = [
    path('workOrder/list/', WorkOrderListView.as_view(), name='work-order-list'),
    path('workOrderStaff/list/', WorkOrderStaffListView.as_view(), name='work-order-staff-list'),
    # 如果需要可浏览的 API，可以添加以下内容
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
print(urlpatterns)
