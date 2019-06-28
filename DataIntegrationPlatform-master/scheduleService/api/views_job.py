# from api.baseViewSet import BaseViewSet
from rest_framework import viewsets, status

from api.serializers import *
from api.views import MyPageNumberPagination, MyJsonResponse


class JobViewSet(viewsets.ModelViewSet):
    """
        作业相关API
        list:
            输出作业列表
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    # def __init__(self):
    #     self._queryset = Task.objects.all()
    #     self._serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        """
        查询作业列表
        return:作业列表
        """
        page_index = request.query_params.get('page_index') if request.query_params.get('page_index') else 1
        page_size = request.query_params.get('page_size') if request.query_params.get('page_size') else 10
        searchWord = request.query_params.get('searchWord')

        self._queryset = self.get_queryset()
        if searchWord:
            self._queryset = self._queryset.filter(taskName__contains=searchWord)
        self._queryset = self.filter_queryset(self._queryset).order_by('taskId')

        page = MyPageNumberPagination()
        page_res = page.paginate_queryset(self._queryset, request)
        # 增加总数量字段
        if page_res is not None:
            serializer = self.get_serializer(page_res, many=True)
            # return self.get_paginated_response(serializer.data)
            return MyJsonResponse(data=serializer.data, code=200, msg="success", status=status.HTTP_200_OK)

        serializer = self.get_serializer(self._queryset, many=True)
        return MyJsonResponse(data=serializer.data, code=200, msg="success", status=status.HTTP_200_OK)


if __name__ == '__main__':
    jobViewSet = JobViewSet()
    # jobViewSet.queryset
    # jobViewSet.serializer_class.
