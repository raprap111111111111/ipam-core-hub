from django.db import models
from companies.models import Company, Branch, Department, Designation, Shift
from django.conf import settings


class EmployeeStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class EmployeeType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
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
    employee_status = models.ForeignKey(EmployeeStatus, on_delete=models.SET_NULL, null=True, blank=True)
    employee_type = models.ForeignKey(EmployeeType, on_delete=models.SET_NULL, null=True, blank=True)

    employee_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    hired_at = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

# --- New Fields ---
    
    # Basic Info
    profile_photo = models.ImageField(upload_to='employees/photos/%Y/%m/', null=True, blank=True, validators=[validate_image_size, validate_is_image])
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say')
    ], null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=255, blank=True)
    emergency_contact_number = models.CharField(max_length=20, blank=True)
    
    # Employment Details
    hired_at = models.DateField(null=True, blank=True) # Reusing/Renaming your existing field
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    
    # Status & Type (Using Choices for better design)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('terminated', 'Terminated'),
        ('resigned', 'Resigned'),
    ]
    employee_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    TYPE_CHOICES = [
        ('regular', 'Regular'),
        ('probationary', 'Probationary'),
        ('contractual', 'Contractual'),
        ('intern', 'Intern'),
    ]
    employee_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='regular')
    
    # Government IDs (PH Context)
    tax_id = models.CharField(max_length=50, blank=True, verbose_name="TIN")
    sss_no = models.CharField(max_length=50, blank=True, verbose_name="SSS Number")
    philhealth_no = models.CharField(max_length=50, blank=True, verbose_name="PhilHealth Number")
    pagibig_no = models.CharField(max_length=50, blank=True, verbose_name="Pag-IBIG Number")
    
    # Payroll Bank Fields
    bank_name = models.CharField(max_length=100, blank=True)
    bank_account_name = models.CharField(max_length=255, blank=True)
    bank_account_number = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"