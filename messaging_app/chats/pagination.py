# chats/pagination.py
from rest_framework.pagination import PageNumberPagination

class DefaultPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"   # optional, client can override
    max_page_size = 100                   # optional, cap the max
