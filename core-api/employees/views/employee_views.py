from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from employees.models import Employee
from employees.serializers import EmployeeSerializer
from employees.services import EmployeeService
from utils.api_helpers import apply_filters_and_paginate
from ..permissions import CanManageEmployees, IsEmployeeOwner

class EmployeeListCreateView(APIView):
    permission_classes = [IsAuthenticated, CanManageEmployees]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        """Handle GET requests (Standard List)"""
        employees = EmployeeService.list_employees()

      # Strict Multi-Company Filtering
        if not request.user.is_superuser:
            try:
                # 1. Look for the Employee record belonging to this logged-in user
                # We assume the Employee model has a field 'user' and a field 'company'
                user_employee_record = Employee.objects.get(user=request.user)
                user_company_id = user_employee_record.company_id
                
                # 2. Now filter all employees by that company ID
                employees = employees.filter(company_id=user_company_id)
                
            except Employee.DoesNotExist:
                # If Maria isn't even listed as an employee, she sees nothing
                employees = employees.none()

        return apply_filters_and_paginate(self, employees, EmployeeSerializer)

    def post(self, request):
        """Handle POST requests (Create OR Search)"""
        search_keys = ['search', 'offset', 'limit', 'is_filter']
        is_search_request = any(key in request.data for key in search_keys)
        
        if is_search_request:
            employees = EmployeeService.list_employees()

            # Strict Multi-Company Filtering for Search
            if not request.user.is_superuser:
                user_company_id = getattr(request.user, 'company_id', None)
                if user_company_id:
                    employees = employees.filter(company_id=user_company_id)
                else:
                    employees = employees.none()

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
    permission_classes = [IsAuthenticated, IsEmployeeOwner | CanManageEmployees]
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk):
        employee = Employee.objects.filter(pk=pk).first()
        
        # Guard against 404 first
        if not employee:
            return Response({
                "success": False,
                "message": "Employee not found",
                "data": None,
                "errors": "The requested ID does not exist."
            }, status=status.HTTP_404_NOT_FOUND)

        # Multi-Company Validation (Prevent ID Guessing)
        if not request.user.is_superuser:
            user_company_id = getattr(request.user, 'company_id', None)
            if employee.company_id != user_company_id:
                return Response({
                    "success": False,
                    "message": "Access Denied",
                    "errors": "This employee belongs to a different company."
                }, status=status.HTTP_403_FORBIDDEN)

        self.check_object_permissions(request, employee)
            
        serializer = EmployeeSerializer(employee)
        return Response({
            "success": True,
            "message": "Employee retrieved successfully",
            "data": serializer.data,
            "errors": None
        })

    def put(self, request, pk):
        """Handle Full Updates"""
        employee = Employee.objects.filter(pk=pk).first()
        if not employee:
            return Response({"success": False, "message": "Not found"}, status=404)

        # Re-use the same company check logic
        if not request.user.is_superuser:
            user_emp = Employee.objects.filter(user=request.user).first()
            if not user_emp or employee.company_id != user_emp.company_id:
                return Response({"success": False, "message": "Access Denied"}, status=403)

        # Update the instance
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            # Use your service to save
            updated_emp = EmployeeService.update_employee(employee, serializer.validated_data)
            return Response({
                "success": True, 
                "message": "Employee updated successfully", 
                "data": EmployeeSerializer(updated_emp).data
            })
        return Response({"success": False, "errors": serializer.errors}, status=400)