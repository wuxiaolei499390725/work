"""scheduleService URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api import views, views_job, views_server
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
# router.register(r'tasks', views.TasksView, base_name='')
router.register(r'tasks', views.TaskViewSet)
router.register(r'monitor/tasks', views_job.JobViewSet)
router.register(r'servers', views_server.ServerViewSet)
# router.register(r'tasklog/v1', views.TaskLogViewSet)
# router.register(r'dataSrc/v1', views.DataSourceViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="国信数据集成平台API文档",
      default_version='v1',
      description="国信数据集成平台API文档",
      # terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="wanghaiying@zork.com.cn"),
      # license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^$', view.hello)，
    # path('hello/', view.hello),
    # url(r'^v1/', include('api.urls')),
    url(r'^v1/', include(router.urls)),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include_docs_urls(title='国信数据集成平台API文档')),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]