from rest_framework import viewsets, status

from api.serializers import *
from api.views import MyPageNumberPagination, MyJsonResponse


class ServerViewSet(viewsets.ModelViewSet):
    """
        服务器相关API
    """
    queryset = Server.objects.all()
    serializer_class = ServerSerializer

    def list(self, request, *args, **kwargs):
        """
        查询服务器列表
        return:服务器列表
        """
        page_index = request.query_params.get('page_index') if request.query_params.get('page_index') else 1
        page_size = request.query_params.get('page_size') if request.query_params.get('page_size') else 10
        business = request.query_params.get('business')

        queryset = self.get_queryset()
        if business:
            queryset = queryset.filter(business=business)
        queryset = self.filter_queryset(queryset).order_by('server_id')

        page = MyPageNumberPagination()
        page_res = page.paginate_queryset(queryset, request)
        # 增加总数量字段
        if page_res is not None:
            serializer = self.get_serializer(page_res, many=True)
            # 增加分页信息
            page_info = dict()
            page_info['total_count'] = queryset.count()
            page_info['page_size'] = page_size
            page_info['page_index'] = page_index
            result = dict()
            result['items'] = serializer.data
            result['page_info'] = page_info
            return MyJsonResponse(data=result, code=200, msg="success", status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return MyJsonResponse(data=serializer.data, code=200, msg="success", status=status.HTTP_200_OK)
