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
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'save/', views.ModelTest.save),
    url(r'query/', views.ModelTest.query),
    url(r'delete/', views.ModelTest.delete),

    # url(r'task/', views.TaskBusiness.testInsertTaskByTransaction),
    url(r'^briefinfo/(?P<taskType>\w+)/$',views.briefInfodetail.as_view()),

    url(r'add/', views.task_test),
]
