from django.urls import path
from .views import DictTypeListView, DictDataListView

# 创建路由器并注册我们的视图集
# router = routers.DefaultRouter()
# router.register(r'dict-type', DictTypeViewSet)
# router.register(r'dict-data', DictDataViewSet)  # 新增 DictData 视图集

# API URL 现在由路由器自动确定
urlpatterns = [
    # path('', include(router.urls)),
    path('dictType/list/', DictTypeListView.as_view(), name='dict-type-list'),
    path('dictData/list/', DictDataListView.as_view(), name='dict-data-list'),
    # 如果需要可浏览的 API，可以添加以下内容
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
