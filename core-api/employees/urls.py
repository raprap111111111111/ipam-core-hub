from django.urls import path
from .views import (
    EmployeeListCreateView, 
    EmployeeDetailView, 
    EmployeeBulkDeleteView  # Make sure to import the new view
)
from employees.views import OrganizationMetadataView

urlpatterns = [
    path('', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('metadata/', OrganizationMetadataView.as_view(), name='org-metadata'),
    path('bulk-delete/', EmployeeBulkDeleteView.as_view(), name='employee-bulk-delete'), # Check this slash!
    path('<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'), # Check this slash!
]