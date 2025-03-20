from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPageNumberPagination(PageNumberPagination):
    # page_query_param = "" url中代表页码的变量名，默认为page
    page_size = 5  # 每一页显示的数据量，没有设置页码，则不进行分页
    # 允许客户端通过指定的参数名来设置每一页数据量的大小，默认是size
    page_size_query_param = "size"  # url单页的数据条数
    max_page_size = 20  # 限制每一页最大展示的数据量

    # 自定义分页返回数据 前端用response.data.data获取课程数据 (如果没有自定义则用response.data.result)
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'data': data,
        })