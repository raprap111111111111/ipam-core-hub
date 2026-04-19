from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from ..permissions import IsCompanyAdmin, BelongsToCompany

from utils.api_helpers import apply_filters_and_paginate
from companies.serializers import ( 
    CompanySerializer, 
    DepartmentSerializer, 
    BranchSerializer, 
    DesignationSerializer
)
from companies.services import (
    CompanyService, 
    DepartmentService, 
    BranchService, 
    DesignationService
)

# Helper to check if a POST request is actually a search/filter request
def is_search(data):
    search_keys = ['search', 'offset', 'limit', 'is_filter', 'ordering']
    return any(key in data for key in search_keys)

# --- COMPANY DETAIL VIEW ---

# --- COMPANY LIST/CREATE VIEW ---

class CompanyListCreateView(APIView):
    permission_classes = [IsAuthenticated] 
    authentication_classes = [JWTAuthentication]

    def get(self, request):
            companies = CompanyService.list_companies()
            # Add search_fields here ↓↓↓
            return apply_filters_and_paginate(
                self, 
                companies, 
                CompanySerializer, 
                search_fields=['name', 'registration_number', 'code', 'address']  # ← ADD THIS
            )

    def post(self, request):
            # Helper to check for search/filter
            if is_search(request.data):
                companies = CompanyService.list_companies()
                # Add search_fields here too ↓↓↓
                return apply_filters_and_paginate(
                    self, 
                    companies, 
                    CompanySerializer, 
                    search_fields=['name', 'registration_number', 'code', 'address']  # ← ADD THIS
                )

            serializer = CompanySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            company = CompanyService.create_company(serializer.validated_data)
            return Response({
                "success": True,
                "message": "Company created successfully",
                "data": CompanySerializer(company).data,
                "errors": None
            }, status=status.HTTP_201_CREATED)
            
class CompanyDetailView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyAdmin]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request, pk):
        try:
            company = CompanyService.get_company(pk)
            return Response({
                "success": True,
                "message": "Company retrieved successfully",
                "data": CompanySerializer(company).data,
                "errors": None
            })
        except Exception:
            return Response({
                "success": False,
                "message": "Company not found",
                "data": None,
                "errors": f"Company with ID {pk} does not exist."
            }, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        # This allows POST to act as PUT for file compatibility
        return self.put(request, pk)

    def patch(self, request, pk):
        return self.put(request, pk)

    def put(self, request, pk):
        try:
            company = CompanyService.get_company(pk)
            # partial=True is what allows PATCH to work
            serializer = CompanySerializer(company, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_company = CompanyService.update_company(pk, serializer.validated_data)
            return Response({
                "success": True,
                "message": "Company updated successfully",
                "data": CompanySerializer(updated_company).data,
                "errors": None
            })
        except Exception as e:
            return Response({
                "success": False,
                "message": "Update failed",
                "data": None,
                "errors": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            company = CompanyService.get_company(pk) # Get it first
            self.check_object_permissions(request, company) # Check it
            CompanyService.delete_company(pk)
            return Response({
                "success": True,
                "message": "Company deleted successfully",
                "data": None,
                "errors": None
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                "success": False,
                "message": "Delete failed",
                "data": None,
                "errors": "Resource not found"
            }, status=status.HTTP_404_NOT_FOUND)

# --- DEPARTMENT VIEWS ---

class DepartmentListCreateView(APIView):
    permission_classes = [IsAuthenticated, BelongsToCompany]
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
