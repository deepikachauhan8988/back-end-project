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


# Admin + Employee Login API
class EmployeeLoginView(APIView):

    def post(self, request):

        serializer = EmployeeLoginSerializer(data=request.data)

        if serializer.is_valid():

            employee = serializer.validated_data["employee"]

            # Admin Login
            if employee.role == "admin":

                return Response({

                    "status": True,
                    "message": "Admin Login Successful",
                    "role": employee.role,
                    "regi_id": employee.regi_id,
                    "access_token": serializer.validated_data['access'],
                    "refresh_token": serializer.validated_data['refresh'],

                }, status=status.HTTP_200_OK)

            # Employee Login
            elif employee.role == "employee":

                return Response({

                    "status": True,
                    "message": "Employee Login Successful",
                    "regi_id": employee.regi_id,

                    "access_token": serializer.validated_data['access'],
                    "refresh_token": serializer.validated_data['refresh'],

                }, status=status.HTTP_200_OK)

        return Response({
            "status": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# List all employees
class EmployeeListView(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)


# Retrieve employee details by regi_id
class EmployeeDetailView(APIView):
    def get(self, request, regi_id):
        try:
            employee = Employee.objects.get(regi_id=regi_id)
        except Employee.DoesNotExist:
            return Response({"status": False, "message": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)