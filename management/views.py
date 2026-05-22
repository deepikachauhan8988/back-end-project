# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Employee
from .serializers import EmployeeSerializer, EmployeeLoginSerializer


# Register API
class EmployeeRegisterView(APIView):

    def post(self, request):

        serializer = EmployeeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "status": True,
                "message": "Employee Registered Successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# Login API
class EmployeeLoginView(APIView):

    def post(self, request):

        serializer = EmployeeLoginSerializer(data=request.data)

        if serializer.is_valid():

            employee = serializer.validated_data["employee"]

            return Response({

                "status": True,
                "message": "Login Successful",

                "employee_id": employee.id,
                "name": employee.name,
                "email": employee.email,
                "department": employee.department,
                "regi_id": employee.regi_id,

                # JWT Tokens
                "access_token": serializer.validated_data['access'],
                "refresh_token": serializer.validated_data['refresh'],

            }, status=status.HTTP_200_OK)

        return Response({
            "status": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
class EmployeeListView(APIView):

    def get(self, request):

        regi_id = request.GET.get('regi_id')

        # Particular Employee
        if regi_id:

            try:
                employee = Employee.objects.get(regi_id=regi_id)

                serializer = EmployeeSerializer(employee)

                return Response({
                    "status": True,
                    "message": "Particular Employee Data",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)

            except Employee.DoesNotExist:

                return Response({
                    "status": False,
                    "message": "Employee Not Found"
                }, status=status.HTTP_404_NOT_FOUND)

        # All Employees
        employees = Employee.objects.all().order_by('-id')

        serializer = EmployeeSerializer(employees, many=True)

        return Response({
            "status": True,
            "message": "All Employee Data",
            "total_employee": employees.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class EmployeeDetailView(APIView):

    def get(self, request, regi_id):
        try:
            employee = Employee.objects.get(regi_id=regi_id)
        except Employee.DoesNotExist:
            return Response({
                "status": False,
                "message": "Employee Not Found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeSerializer(employee)

        return Response({
            "status": True,
            "message": "Particular Employee Data",
            "data": serializer.data
        }, status=status.HTTP_200_OK)