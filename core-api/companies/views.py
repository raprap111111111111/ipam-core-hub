from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from utils.api_helpers import apply_filters_and_paginate
from .serializers import (
    CompanySerializer, 
    DepartmentSerializer, 
    BranchSerializer, 
    DesignationSerializer
)
from .services import (
    CompanyService, 
    DepartmentService, 
    BranchService, 
    DesignationService
)

# Helper to check if a POST request is actually a search/filter request
def is_search(data):
    search_keys = ['search', 'offset', 'limit', 'is_filter', 'ordering']
    return any(key in data for key in search_keys)

# --- COMPANY VIEWS ---

class CompanyListCreateView(APIView):
    permission_classes = [IsAuthenticated] 
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        companies = CompanyService.list_companies()
        return apply_filters_and_paginate(self, companies, CompanySerializer)

    def post(self, request):
        if is_search(request.data):
            companies = CompanyService.list_companies()
            return apply_filters_and_paginate(self, companies, CompanySerializer)

        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = CompanyService.create_company(serializer.validated_data)
        return Response({
            "success": True,
            "message": "Company created successfully",
            "data": CompanySerializer(company).data,
            "errors": None
        }, status=status.HTTP_201_CREATED)

# --- DEPARTMENT VIEWS ---

class DepartmentListCreateView(APIView):
    permission_classes = [IsAuthenticated] 
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        departments = DepartmentService.list_departments()
        # Fixed: Searchable fields for Department
        return apply_filters_and_paginate(self, departments, DepartmentSerializer, search_fields=['name', 'code'])

    def post(self, request):
        if is_search(request.data):
            departments = DepartmentService.list_departments()
            # Fixed: Searchable fields for Department
            return apply_filters_and_paginate(self, departments, DepartmentSerializer, search_fields=['name', 'code'])

        serializer = DepartmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        department = DepartmentService.create_department(serializer.validated_data)
        return Response({
            "success": True,
            "message": "Department created successfully",
            "data": DepartmentSerializer(department).data,
            "errors": None
        }, status=status.HTTP_201_CREATED)

class DepartmentDetailView(APIView):
    permission_classes = [IsAuthenticated] 
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk):
        try:
            department = DepartmentService.get_department(pk)
            return Response({
                "success": True,
                "message": "Department retrieved successfully",
                "data": DepartmentSerializer(department).data,
                "errors": None
            })
        except Exception:
            return Response({
                "success": False,
                "message": "Department not found",
                "data": None,
                "errors": "The requested ID does not exist."
            }, status=status.HTTP_404_NOT_FOUND)

# --- BRANCH VIEWS ---

class BranchListCreateView(APIView):
    permission_classes = [IsAuthenticated] 
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        branches = BranchService.list_branches()
        # Searchable fields for Branch
        return apply_filters_and_paginate(self, branches, BranchSerializer, search_fields=['name', 'code'])

    def post(self, request):
        if is_search(request.data):
            branches = BranchService.list_branches()
            return apply_filters_and_paginate(self, branches, BranchSerializer, search_fields=['name', 'code'])

        serializer = BranchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        branch = BranchService.create_branch(serializer.validated_data)
        return Response({
            "success": True,
            "message": "Branch created successfully",
            "data": BranchSerializer(branch).data,
            "errors": None
        }, status=status.HTTP_201_CREATED)

class BranchDetailView(APIView):
    permission_classes = [IsAuthenticated] 
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk):
        try:
            branch = BranchService.get_branch(pk)
            return Response({
                "success": True,
                "message": "Branch retrieved successfully",
                "data": BranchSerializer(branch).data,
                "errors": None
            })
        except Exception:
            return Response({
                "success": False,
                "message": "Branch not found",
                "data": None,
                "errors": "The requested ID does not exist."
            }, status=status.HTTP_404_NOT_FOUND)

# --- DESIGNATION VIEWS ---

class DesignationListCreateView(APIView):
    permission_classes = [IsAuthenticated] 
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        designations = DesignationService.list_designations()
        # Searchable fields for Designation
        return apply_filters_and_paginate(self, designations, DesignationSerializer, search_fields=['name', 'code'])

    def post(self, request):
        if is_search(request.data):
            designations = DesignationService.list_designations()
            return apply_filters_and_paginate(self, designations, DesignationSerializer, search_fields=['name', 'code'])

        serializer = DesignationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        designation = DesignationService.create_designation(serializer.validated_data)
        return Response({
            "success": True,
            "message": "Designation created successfully",
            "data": DesignationSerializer(designation).data,
            "errors": None
        }, status=status.HTTP_201_CREATED)

class DesignationDetailView(APIView):
    permission_classes = [IsAuthenticated] 
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk):
        try:
            designation = DesignationService.get_designation(pk)
            return Response({
                "success": True,
                "message": "Designation retrieved successfully",
                "data": DesignationSerializer(designation).data,
                "errors": None
            })
        except Exception:
            return Response({
                "success": False,
                "message": "Designation not found",
                "data": None,
                "errors": "The requested ID does not exist."
            }, status=status.HTTP_404_NOT_FOUND)