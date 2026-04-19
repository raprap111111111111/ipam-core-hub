from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    code = models.CharField(max_length=50, unique=True, blank=True, null=True)

    # ✅ NEW: Company Logo
    logo = models.ImageField(
        upload_to='company_logos/', 
        blank=True, 
        null=True,
        help_text="Company logo image"
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"



class Branch(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('branch', 'name')

    def __str__(self):
        return self.name

       


class Designation(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='designations')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Shift(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='shifts')
    name = models.CharField(max_length=255)
    time_in = models.TimeField()
    time_out = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name