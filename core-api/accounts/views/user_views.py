from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from ..permissions import IsAdminUser, IsAccountOwner

from ..serializers import (
    LoginSerializer, LogoutSerializer, 
    ChangePasswordSerializer, UserMeSerializer
)

User = get_user_model()

class LoginView(APIView):
    permission_classes = []
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserMeSerializer(user).data
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logged out.'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Force a refresh from the DB to catch the new Group permissions
        user = request.user
        
        # This ensures Django re-calculates permissions from the Groups
        # instead of using what's already in memory
        serializer = UserMeSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Add this new view to list the permissions (IDs 1-72 etc.)
class PermissionListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        perms = Permission.objects.all().values('id', 'name', 'codename', 'content_type__app_label')
        return Response(perms, status=status.HTTP_200_OK)

# Update this view to ONLY handle Role IDs and Role updates
class RolePermissionView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """ Returns [{"id": 1, "name": "HR_ADMIN"}, ...] """
        roles = Group.objects.all().values('id', 'name')
        return Response(list(roles), status=status.HTTP_200_OK)

    def post(self, request):
        role_id = request.data.get('role_id')
        permission_ids = request.data.get('permissions', [])
        
        try:
            role = Group.objects.get(id=role_id)
            perms = Permission.objects.filter(id__in=permission_ids)
            role.permissions.set(perms)
            return Response({
                "message": f"Permissions updated for {role.name}",
                "role_id": role.id
            }, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)
            
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'message': 'Success'})

class AssignRoleView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        user_id = request.data.get('user_id')
        role_id = request.data.get('role_id') # Changed from role_name to role_id

        try:
            user = User.objects.get(id=user_id)
            group = Group.objects.get(id=role_id)
            
            # Optional: Log the old roles before clearing
            old_roles = list(user.groups.values_list('name', flat=True))
            
            # Remove all current roles
            user.groups.clear() 
            
            # Add the new role
            user.groups.add(group)
            
            return Response({
                "message": "Role assigned successfully",
                "user": user.email,
                "previous_roles": old_roles,
                "new_role": group.name
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({"error": "Role ID does not exist"}, status=status.HTTP_404_NOT_FOUND)

# Add this to the bottom of accounts/views/user_views.py
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAccountOwner]
    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)

class UserRegistrationView(APIView):
    permission_classes = []
    def post(self, request):
        # Your registration logic here
        return Response({"message": "User registered"}, status=status.HTTP_201_CREATED)