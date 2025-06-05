"""
URL configuration for wos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # 语言切换视图
    path('rest/auth/', include('users.urls')),  # 认证Rest接口
    path('rest/system/', include('system.urls')),  # 系统Rest接口
    path('rest/workOrder/', include('work_order.urls')),  # 工单Rest接口
    path('', admin.site.urls),  # 添加空路径规则

]
