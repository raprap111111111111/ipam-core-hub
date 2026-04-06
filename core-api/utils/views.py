from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

# Custom Pagination Class (Optional: if you want to change the JSON structure)
class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class BaseListAPIView(generics.ListAPIView):
    """
    Global Base View for all 'Get All' endpoints.
    Includes Filtering, Search, Sorting, and Pagination by default.
    """
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # These will be overridden in the actual view
    filterset_fields = []
    search_fields = []
    ordering_fields = '__all__' 
    ordering = ['-id'] # Default sort