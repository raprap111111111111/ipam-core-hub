from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from dashboard.services.dashboard_services import DashboardService
from dashboard.serializers.dashboard_serializers import DashboardSummarySerializer


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        dashboard_data = DashboardService.get_summary(request.user)
        serializer = DashboardSummarySerializer(dashboard_data)
        

        return Response({
            "success": True,
            "message": "Dashboard data retrieved successfully",
            "data": serializer.data,
            "errors": None,
        })