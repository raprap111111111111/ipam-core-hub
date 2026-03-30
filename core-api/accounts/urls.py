from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    LoginView, LogoutView, ChangePasswordView, 
    MeView, AssignRoleView, RolePermissionView,
    PermissionListView  # <--- Add this import (Make sure to create this view!)
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('assign-role/', AssignRoleView.as_view(), name='assign-role'),
    
    # 1. Use this to GET all Role IDs (1, 2, 3) AND POST to update them
    path('roles/', RolePermissionView.as_view(), name='role-list-update'),
    
    # 2. Use this to GET the big list of all system permissions (33, 34, 35...)
    path('permissions/', PermissionListView.as_view(), name='permissions-list'),
]