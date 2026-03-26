from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     model = User

#     # Added the three name fields here
#     list_display = (
#         'email',
#         'first_name',
#         'last_name',
#         'is_hr_admin',
#         'is_staff',
#         'is_active',
#         'created_at',
#     )

#     list_filter = (
#         'is_hr_admin',
#         'is_staff',
#         'is_active',
#         'is_superuser',
#     )

#     ordering = ('email',)
#     # Search by first or last name now
#     search_fields = ('email', 'first_name', 'last_name')

#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal Info', {
#             'fields': ('first_name', 'middle_name', 'last_name', 'avatar', 'phone_number')
#         }),
#         ('Organization', {'fields': ('company', 'branch', 'employee')}),
#         ('Permissions', {
#             'fields': (
#                 'is_hr_admin',
#                 'is_active',
#                 'is_staff',
#                 'is_superuser',
#                 'groups',
#                 'user_permissions',
#             )
#         }),
#         ('Important Dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
#     )

#     readonly_fields = ('created_at', 'updated_at', 'last_login')

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': (
#                 'email',
#                 'first_name',
#                 'last_name',
#                 'password', # BaseUserAdmin usually uses 'password' for creation
#                 'is_staff',
#                 'is_active',
#             ),
#         }),
#     )