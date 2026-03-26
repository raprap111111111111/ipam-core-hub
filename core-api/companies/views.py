from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import CompanySerializer
from .services import CompanyService


class CompanyListCreateView(APIView):
    def get(self, request):
        companies = CompanyService.list_companies()
        return Response(CompanySerializer(companies, many=True).data)

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = CompanyService.create_company(serializer.validated_data)
        return Response(
            CompanySerializer(company).data,
            status=status.HTTP_201_CREATED
        )