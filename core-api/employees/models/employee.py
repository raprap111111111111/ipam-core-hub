import os
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from companies.models import Company, Branch, Department, Designation, Shift

# 1. Define the missing validators at the top
def validate_image_size(value):
    filesize = value.size
    if filesize > 2 * 1024 * 1024:  # 2MB limit
        raise ValidationError("The maximum file size that can be uploaded is 2MB")
    return value

def validate_is_image(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Use JPG, PNG, or WEBP.')

class EmployeeStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class EmployeeType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Employee(models.Model):
    # --- Relations ---
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='employee_profile',
        null=True, 
        blank=True
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='employees')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')

    # --- Basic Info ---
    employee_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    profile_photo = models.ImageField(
        upload_to='employees/photos/%Y/%m/', 
        null=True, 
        blank=True, 
        validators=[validate_image_size, validate_is_image]
    )
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say')
    ], null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # --- Emergency Contact ---
    emergency_contact_name = models.CharField(max_length=255, blank=True)
    emergency_contact_number = models.CharField(max_length=20, blank=True)
    
    # --- Employment Details ---
    hired_at = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Using the foreign keys you defined at the top
    employee_status = models.ForeignKey(EmployeeStatus, on_delete=models.SET_NULL, null=True, blank=True)
    employee_type = models.ForeignKey(EmployeeType, on_delete=models.SET_NULL, null=True, blank=True)
    
    # --- Government IDs (PH Context) ---
    tax_id = models.CharField(max_length=50, blank=True, verbose_name="TIN")
    sss_no = models.CharField(max_length=50, blank=True, verbose_name="SSS Number")
    philhealth_no = models.CharField(max_length=50, blank=True, verbose_name="PhilHealth Number")
    pagibig_no = models.CharField(max_length=50, blank=True, verbose_name="Pag-IBIG Number")
    
    # --- Payroll Bank Fields ---
    bank_name = models.CharField(max_length=100, blank=True)
    bank_account_name = models.CharField(max_length=255, blank=True)
    bank_account_number = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Using a safer way to get the name if user is null
        if self.user:
            return f"{self.user.first_name} {self.user.last_name}"
        return f"{self.first_name} {self.last_name}"