# employees/views/metadata_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from companies.models import Company, Branch, Department, Designation

class OrganizationMetadataView(APIView):
    def get(self, request):
        # We fetch all companies and their branches in one go
        # This is the "with" equivalent in Django: select_related/prefetch_related
        companies = Company.objects.all().prefetch_related('branches__departments')
        
        # Build a nested structure if you want a true hierarchy, 
        # or just flat lists for dropdowns. 
        # Let's provide flat lists for your current frontend setup:
        
        data = {
            "companies": Company.objects.filter(is_active=True).values('id', 'name'),
            "branches": Branch.objects.filter(is_active=True).values('id', 'name', 'company_id'),
            "departments": Department.objects.filter(is_active=True).values('id', 'name', 'branch_id'),
            "designations": Designation.objects.filter(is_active=True).values('id', 'name')
        }
        
        return Response({
            "success": True,
            "data": data
        })