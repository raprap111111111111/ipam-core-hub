# utils/api_helpers.py
from rest_framework.response import Response
from django.db.models import Q
import math

def apply_filters_and_paginate(view, queryset, serializer_class, search_fields=None):
    request = view.request
    data = request.data if request.data else request.query_params
    
    # 1. Extract Limit (Page Size)
    try:
        limit = int(data.get('limit', 10))
    except (ValueError, TypeError):
        limit = 10

    # 2. Calculate Offset based on 'page' or 'offset'
    page_param = data.get('page')
    offset_param = data.get('offset')

    if page_param:
        try:
            current_page = max(int(page_param), 1)
            offset = (current_page - 1) * limit
        except (ValueError, TypeError):
            offset = 0
    elif offset_param:
        try:
            offset = int(offset_param)
        except (ValueError, TypeError):
            offset = 0
    else:
        offset = 0
        
    # 3. Handle Sorting
    order_by = data.get('order_by', 'id')
    order_dir = data.get('order_dir', 'desc')
    direction = '-' if order_dir == 'desc' else ''
    
    # Apply Search (if search_fields were provided)
    search = data.get('search', '')
    if search and search_fields:
        search_query = Q()
        for field in search_fields:
            search_query |= Q(**{f"{field}__icontains": search})
        queryset = queryset.filter(search_query)

    queryset = queryset.order_by(f"{direction}{order_by}")

    # 4. Pagination Execution
    total_records = queryset.count()
    records = queryset[offset : offset + limit]
    
    # 5. Serialization WITH REQUEST CONTEXT (Fixes the broken Ralph image)
    serialized_records = serializer_class(
        records, 
        many=True, 
        context={'request': request}
    ).data
    
    # 6. Response Meta Calculation
    current_page = (offset // limit) + 1
    last_page = math.ceil(total_records / limit) if total_records > 0 else 1
    has_more = offset + limit < total_records

    return Response({
        "success": True,
        "message": "Records retrieved successfully",
        "data": {
            "total": total_records,
            "records": serialized_records,
            "offset": offset,
            "limit": limit,
            "current_page": current_page,
            "last_page": last_page,
            "per_page": limit,
            "has_more": has_more
        },
        "errors": None
    })