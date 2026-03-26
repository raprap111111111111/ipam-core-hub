from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import AttendanceSerializer
from .services import AttendanceService


class AttendanceListCreateView(APIView):
    def get(self, request):
        attendance = AttendanceService.list_attendance()
        return Response(AttendanceSerializer(attendance, many=True).data)

    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        attendance = AttendanceService.create_attendance(serializer.validated_data)
        return Response(
            AttendanceSerializer(attendance).data,
            status=status.HTTP_201_CREATED
        )