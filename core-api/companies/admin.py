from django.contrib import admin
from .models import Company, Branch, Department, Designation, Shift

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active')

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'code', 'is_active')
    list_filter = ('company',)

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'time_in', 'time_out')
    
# Keep the simple ones for the smaller models
admin.site.register(Department)
admin.site.register(Designation)