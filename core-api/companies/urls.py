from django.urls import path
from .views import (
    CompanyListCreateView, 
    CompanyDetailView,
    DepartmentListCreateView, 
    DepartmentDetailView,
    BranchListCreateView, 
    BranchDetailView,
    DesignationListCreateView,
    DesignationDetailView
)

urlpatterns = [
path('', CompanyListCreateView.as_view(), name='company-list-create'),
    path('<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),

    path('departments/', DepartmentListCreateView.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', DepartmentDetailView.as_view(), name='dept-detail'), 

    path('branches/', BranchListCreateView.as_view(), name='branch-list-create'),
     path('branches/<int:pk>/', BranchDetailView.as_view(), name='branch-detail'), 
    


    path('designations/', DesignationListCreateView.as_view(), name='designation-list-create'),
     path('designations/<int:pk>/', DesignationDetailView.as_view(), name='designation-detail'), 
]