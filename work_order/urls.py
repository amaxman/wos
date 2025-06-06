from django.urls import path
from .views import WorkOrderListView, WorkOrderStaffListView, WorkOrderRetrieveUpdateDestroyView, \
    WorkOrderStaffRetrieveUpdateDestroyView

# API URL 现在由路由器自动确定
urlpatterns = [
    path('workOrder/list/', WorkOrderListView.as_view(), name='work-order-list'),
    path('workOrder/<int:pk>/', WorkOrderRetrieveUpdateDestroyView.as_view(),
         name='work-order-retrieve-update-destroy'),
    path('workOrderStaff/list/', WorkOrderStaffListView.as_view(), name='work-order-staff-list'),
    path('workOrderStaff/<int:pk>/', WorkOrderStaffRetrieveUpdateDestroyView.as_view(),
         name='work-order-staff-retrieve-update-destroy'),
]
