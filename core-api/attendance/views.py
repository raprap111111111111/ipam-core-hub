from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import AttendanceSerializer
from .services import AttendanceService
from utils.api_helpers import apply_filters_and_paginate


class AttendanceListCreateView(APIView):
    def get(self, request):
        attendance = AttendanceService.list_attendance()
        return apply_filters_and_paginate(
            self, 
            attendance, 
            AttendanceSerializer, 
            # FIX: Use the actual database fields on the related model
            search_fields=['employee__first_name', 'employee__last_name', 'status'] 
        )

    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        attendance = AttendanceService.create_attendance(serializer.validated_data)
        return Response(
            AttendanceSerializer(attendance).data,
            status=status.HTTP_201_CREATED
        )