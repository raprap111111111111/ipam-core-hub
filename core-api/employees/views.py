from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Employee
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import EmployeeSerializer
from .services import EmployeeService


class EmployeeListCreateView(APIView):
    # This forces the user to be logged in
    permission_classes = [IsAuthenticated] 
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        employees = EmployeeService.list_employees()
        return Response(EmployeeSerializer(employees, many=True).data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee = EmployeeService.create_employee(serializer.validated_data)
        return Response(
            EmployeeSerializer(employee).data,
            status=status.HTTP_201_CREATED
        )

class EmployeeDetailView(APIView):

        # This forces the user to be logged in
    permission_classes = [IsAuthenticated] 
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk):
        try:
            # Look up the employee by the primary key (pk)
            employee = Employee.objects.get(pk=pk)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)