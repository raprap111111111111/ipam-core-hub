from rest_framework.response import Response
from django.db.models import Q
import math

def apply_filters_and_paginate(view, queryset, serializer_class, search_fields=None):
    request = view.request
    # Check POST data first, fallback to GET query params
    data = request.data if request.data else request.query_params
    
    # Extract Params
    search = data.get('search', '')
    try:
        offset = int(data.get('offset', 0))
        limit = int(data.get('limit', 10))
    except (ValueError, TypeError):
        offset = 0
        limit = 10
        
    order_by = data.get('order_by', 'id')
    order_dir = data.get('order_dir', 'desc')

    # Apply Search - Now search_fields is correctly passed as an argument
    if search and search_fields:
        search_query = Q()
        for field in search_fields:
            search_query |= Q(**{f"{field}__icontains": search})
        queryset = queryset.filter(search_query)

    # Apply Sorting
    direction = '-' if order_dir == 'desc' else ''
    queryset = queryset.order_by(f"{direction}{order_by}")

    # Pagination
    total_records = queryset.count()
    records = queryset[offset : offset + limit]
    
    current_page = (offset // limit) + 1
    last_page = math.ceil(total_records / limit) if total_records > 0 else 1
    has_more = offset + limit < total_records

    return Response({
        "success": True,
        "message": "Records retrieved successfully",
        "data": {
            "total": total_records,
            "records": serializer_class(records, many=True).data,
            "offset": offset,
            "limit": limit,
            "current_page": current_page,
            "last_page": last_page,
            "per_page": limit,
            "has_more": has_more
        },
        "errors": None
    })