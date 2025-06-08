from django.urls import path
from .views import DictTypeListView, DictDataListView, DictTypeRetrieveUpdateDestroyView, \
    DictDataRetrieveUpdateDestroyView, DictTypeListCreateView,DictDataListCreateView

# 创建路由器并注册我们的视图集
# router = routers.DefaultRouter()
# router.register(r'dict-type', DictTypeViewSet)
# router.register(r'dict-data', DictDataViewSet)  # 新增 DictData 视图集

# API URL 现在由路由器自动确定
urlpatterns = [
    # path('', include(router.urls)),
    path('dictType/list/', DictTypeListView.as_view(), name='dict-type-list'),
    # Dict Type Create，如果不需要，可删除
    path('dictType/', DictTypeListCreateView.as_view(), name='dict-type-create'),
    path('dictType/<int:pk>/', DictTypeRetrieveUpdateDestroyView.as_view(), name='dict-type-retrieve-update-destroy'),
    path('dictData/list/', DictDataListView.as_view(), name='dict-data-list'),
    # Dict Data Create，如果不需要，可删除
    path('dictData/', DictDataListCreateView.as_view(), name='dict-data-create'),
    path('dictData/<int:pk>/', DictDataRetrieveUpdateDestroyView.as_view(), name='dict-data-retrieve-update-destroy'),
]
