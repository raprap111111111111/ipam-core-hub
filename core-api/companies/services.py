from .models import Company


class CompanyService:
    @staticmethod
    def list_companies():
        return Company.objects.all()

    @staticmethod
    def create_company(data):
        return Company.objects.create(**data)