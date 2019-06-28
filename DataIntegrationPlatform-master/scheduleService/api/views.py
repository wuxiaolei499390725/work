from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .models import *
from rest_framework import viewsets, mixins, status
from api.serializers import *
from rest_framework.views import APIView
from django.utils import six
from rest_framework.pagination import PageNumberPagination


class MyPageNumberPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 50
    page_size_query_param = 'page_size'
    page_query_param = 'page_index'


class MyJsonResponse(Response):
    """
    An HttpResponse that allows its data to be rendered into arbitrary media types.
    """
    def __init__(self, data=None, code=None, msg=None, status=None, template_name=None, headers=None, exception=False, content_type=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.
        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super(Response, self).__init__(None, status=status)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)

        self.data = {"code": code, "message": msg, "data": data}
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in six.iteritems(headers):
                self[name] = value


class TaskViewSet(viewsets.ModelViewSet):
    """
        任务相关API

        list:
            输出任务列表
        create:
            创建任务
        retrieve:
            查询任务详情
        update:
            更新任务信息
        destroy:
            删除任务
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        """
        查询任务列表
        return:任务列表
        """
        page_index = request.query_params.get('page_index') if request.query_params.get('page_index') else 1
        page_size = request.query_params.get('page_size') if request.query_params.get('page_size') else 10
        task_name = request.query_params.get('task_name')
        table_name = request.query_params.get('table_name')
        task_type = request.query_params.get('task_type')
        task_status = request.query_params.get('task_status')
        dataSrcName = request.query_params.get('dataSrcName')
        dataDestName = request.query_params.get('dataDestName')

        # queryset = self.filter_queryset(self.get_queryset().order_by('taskId'))
        queryset = self.get_queryset()
        if task_name:
            queryset = queryset.filter(taskName__contains=task_name)
        if task_type:
            queryset = queryset.filter(taskType=task_type)
        if task_status:
            queryset = queryset.filter(enabled=task_status)
        queryset = self.filter_queryset(queryset).order_by('taskId')

        page = MyPageNumberPagination()
        page_res = page.paginate_queryset(queryset, request)

        if page_res is not None:
            serializer = self.get_serializer(page_res, many=True)
            # return self.get_paginated_response(serializer.data)
            # 增加分页信息
            page_info = dict()
            page_info['totalCount'] = queryset.count()
            page_info['page_size'] = page_size
            page_info['page_index'] = page_index

            result = dict()
            result['items'] = serializer.data
            result['page_info'] = page_info
            return MyJsonResponse(data=result, code=200, msg="success", status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        # 增加分页信息
        page_info = dict()
        page_info['totalCount'] = queryset.count()
        page_info['page_size'] = page_size
        page_info['page_index'] = page_index

        result = dict()
        result['items'] = serializer.data
        result['page_info'] = page_info
        return MyJsonResponse(data=result, code=200, msg="success", status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return MyJsonResponse(data=serializer.data, msg="success", code=201, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return MyJsonResponse(data=serializer.data, code=200, msg="success", status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return MyJsonResponse(data=serializer.data, msg="success", code=200, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        serializer = self.get_serializer(instance)
        return MyJsonResponse(data=serializer.data, code=204, msg="delete resource success", status=status.HTTP_204_NO_CONTENT)


class DataSourceViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class EtlServerViewSet(viewsets.ModelViewSet):
    queryset = EtlServer.objects.all()
    serializer_class = EtlServerSerializer


class TaskLogViewSet(viewsets.ModelViewSet):
    queryset = TaskLog.objects.all()
    serializer_class = TaskLogSerializer


class ModelTest:
    def save(self):
        test1 = PreTask(task_id=2, PreTask_id=2)
        test1.save()
        return HttpResponse("<p>数据添加成功！</p>")

    def query(self):
        res = PreTask.objects.filter(task_id=2)
        return HttpResponse("<p>" + str(res) + "</p>")

    def delete(self):
        test1 = PreTask(task_id=1, PreTask_id=2)
        test1.delete()
        return HttpResponse("<p>数据删除成功！</p>")


class TaskBusiness:
    # task 任务数据
    # srcTasks 源表数据
    # destTasks 目的表数据
    # PreTasks 前置任务数据
    # scheduleTasks 自定义周期数据
    def insert_task(self, task, srcTasks, destTasks, PreTasks, scheduleTasks):
        # 任务表数据入库
        task.save()

        task_id = task.taskId if task.taskId else -1
        res = "task_id:%s" % task_id

        # 源表数据入库
        # for srcTask in srcTasks:
        #     srcTask.save()
        srcTasks.save()

        # 目的表数据入库
        # for destTask in destTasks:
        #     destTask.save()
        destTasks.save()

        # 前置任务表数据入库
        # for PreTask in PreTasks:
        #     PreTask.task_id = task_id;
        #     PreTask.save()
        PreTasks.save()

        # 自定义周期表数据入库
        # for scheduleTask in scheduleTasks:
        #     scheduleTask.save()
        scheduleTasks.save()

        return res

    def test_insert_task(self):
        # print(PreTask)
        task = Task(taskId=1, etlserverip='0.0.0.0', taskname='test', executiontype='test', tasktype='test',
                    scheduletype='test', startexecutedateid=1, enabled=1)
        srcTasks = TaskSrcTable(tasksrctableid=1, task_id=1, srctableid=1)
        destTasks = TaskDestTable(taskdesttableid=1, task_id=1, desttableid=1)
        PreTasks = PreTask(task_id=1, PreTask_id=2)
        scheduleTasks = Schedule(originaldate='2019-05-22 00:00:00', dateid=1, istradedate=1, isweeklydate=1,
                                 ismonthlydate=1, memo='test')

        res = TaskBusiness.insert_task(self, task, srcTasks, destTasks, PreTasks, scheduleTasks)
        return HttpResponse("ok")

    def update_task(self):
        return

    def delete_task(self):
        return

    def get_srctable_by_task_id(self):
        return

    def get_desttable_by_task_id(self):
        return

    def get_PreTask_by_task_id(self):
        return

    def get_schedule_by_task_id(self):
        return


from django.http import JsonResponse
# from api.guosenCelery import *
from .celeryTasks import *


# def index(request,*args,**kwargs):
#     res = add.delay(1,3)
# 任务逻辑
# return JsonResponse({'status':'successful','task_id':res.task_id})

class briefInfodetail(APIView):
    def get(self,request, taskType):
        briefInfo_obj = briefinfo.objects.filter(taskType=taskType)
        brf = briefInfoSerializers(briefInfo_obj, many=True)
        return JsonResponse(brf.data, safe=False)

def task_test(self):
    # res = add.delay(228, 24)
    res = add.apply_async([1, 2])
    print("start running task add()")
    print("async task res", res.get())

    return HttpResponse('res %s' % res.get())
