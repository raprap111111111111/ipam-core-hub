from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Employee
from .serializers import EmployeeSerializer
from .services import EmployeeService
from utils.api_helpers import apply_filters_and_paginate

class EmployeeListCreateView(APIView):
    permission_classes = [IsAuthenticated] 
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        """Handle GET requests (Standard List)"""
        employees = EmployeeService.list_employees()
        # Use helper so GET also gets the nice success/data structure
        return apply_filters_and_paginate(self, employees, EmployeeSerializer)

    def post(self, request):
        """Handle POST requests (Create OR Search)"""
        # Check if the body contains search/pagination keys
        search_keys = ['search', 'offset', 'limit', 'is_filter']
        is_search_request = any(key in request.data for key in search_keys)
        
        if is_search_request:
            employees = EmployeeService.list_employees()
            return apply_filters_and_paginate(self, employees, EmployeeSerializer)

        # Standard Creation Logic
        serializer = EmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee = EmployeeService.create_employee(serializer.validated_data)
        
        return Response({
            "success": True,
            "message": "Employee created successfully",
            "data": EmployeeSerializer(employee).data,
            "errors": None
        }, status=status.HTTP_201_CREATED)

class EmployeeDetailView(APIView):
    permission_classes = [IsAuthenticated] 
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk):
        employee = Employee.objects.filter(pk=pk).first()
        if not employee:
            return Response({
                "success": False,
                "message": "Employee not found",
                "data": None,
                "errors": "The requested ID does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
            
        serializer = EmployeeSerializer(employee)
        return Response({
            "success": True,
            "message": "Employee retrieved successfully",
            "data": serializer.data,
            "errors": None
        })