from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Add BranchSerializer and DesignationSerializer here
from .serializers import (
    CompanySerializer, 
    DepartmentSerializer, 
    BranchSerializer, 
    DesignationSerializer
)

# Add the missing services here
from .services import (
    CompanyService, 
    DepartmentService, 
    BranchService, 
    DesignationService
)


class CompanyListCreateView(APIView):
    def get(self, request):
        companies = CompanyService.list_companies()
        return Response(CompanySerializer(companies, many=True).data)

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = CompanyService.create_company(serializer.validated_data)
        return Response(CompanySerializer(company).data, status=status.HTTP_201_CREATED)

# ... (imports remain the same)

# 1. This handles /api/companies/departments/ (GET all, POST new)
class DepartmentListCreateView(APIView):
    def get(self, request):
        departments = DepartmentService.list_departments() 
        return Response(DepartmentSerializer(departments, many=True).data)

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        department = DepartmentService.create_department(serializer.validated_data)
        return Response(DepartmentSerializer(department).data, status=status.HTTP_201_CREATED)

# 2. This handles /api/companies/departments/1/ (GET one by ID)
class DepartmentDetailView(APIView):
    def get(self, request, pk):
        try:
            department = DepartmentService.get_department(pk)
            return Response(DepartmentSerializer(department).data)
        except Exception: 
            return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)

        
class BranchListCreateView(APIView):
    def get(self, request):
        branches = BranchService.list_branches()
        return Response(BranchSerializer(branches, many=True).data)

    def post(self, request):
        serializer = BranchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        branch = BranchService.create_branch(serializer.validated_data)
        return Response(BranchSerializer(branch).data, status=status.HTTP_201_CREATED)


        # 2. This handles /api/companies/departments/1/ (GET one by ID)
class BranchDetailView(APIView):
    def get(self, request, pk):
        try:
            branch = BranchService.get_branch(pk)
            return Response(BranchSerializer(branch).data)
        except Exception: 
            return Response({"error": "Branch not found"}, status=status.HTTP_404_NOT_FOUND)

class DesignationListCreateView(APIView):
    def get(self, request):
        designations = DesignationService.list_designations()
        return Response(DesignationSerializer(designations, many=True).data)

    def post(self, request):
        serializer = DesignationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        designation = DesignationService.create_designation(serializer.validated_data)
        return Response(DesignationSerializer(designation).data, status=status.HTTP_201_CREATED)

        # 2. This handles /api/companies/departments/1/ (GET one by ID)
class DesignationDetailView(APIView):
    def get(self, request, pk):
        try:
            designation = DesignationService.get_designation(pk)
            return Response(DesignationSerializer(designation).data)
        except Exception: 
            return Response({"error": "Designation not found"}, status=status.HTTP_404_NOT_FOUND)