from django.core.exceptions import ValidationError

def validate_image_size(fieldfile_obj):
    filesize = fieldfile_obj.size
    megabyte_limit = 2.0  # Limit to 2MB
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"Max file size is {megabyte_limit}MB")

def validate_is_image(fieldfile_obj):
    extension = fieldfile_obj.name.split('.')[-1].lower()
    if extension not in ['jpg', 'jpeg', 'png', 'webp']:
        raise ValidationError("Only JPG, PNG, and WebP images are allowed.")