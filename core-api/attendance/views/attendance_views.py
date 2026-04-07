from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated

from ..permissions import IsAttendanceOwner, CanApproveAttendance
from attendance.serializers import AttendanceSerializer
from attendance.services import AttendanceService
from utils.api_helpers import apply_filters_and_paginate


class AttendanceListCreateView(APIView):
    permission_classes = [IsAuthenticated]

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

class AttendanceDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAttendanceOwner | CanApproveAttendance]
    def get(self, request, pk):
        attendance = AttendanceService.get_attendance(pk)
        return Response(AttendanceSerializer(attendance).data)

    def put(self, request, pk):
        attendance = AttendanceService.update_attendance(pk, request.data)
        return Response(AttendanceSerializer(attendance).data)

    def delete(self, request, pk):
        AttendanceService.delete_attendance(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)