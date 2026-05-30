# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Employee, InterviewQuestion, InterviewAnswer
from .serializers import (
    EmployeeRegistrationSerializer, 
    EmployeeSerializer, 
    EmployeeLoginSerializer,
    InterviewQuestionSerializer,
    InterviewQuestionListSerializer,
    InterviewAnswerSerializer
)


# Register API
class EmployeeRegisterView(APIView):

    def post(self, request):

        serializer = EmployeeRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            employee = serializer.save()

            return Response({
                "status": True,
                "message": "User Registered Successfully",
               
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
                    "message": "User Login Successful",
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


# ==================== INTERVIEW SYSTEM APIs ====================

@api_view(['GET'])
def get_all_categories(request):
    try:
        categories = InterviewQuestion.objects.values_list('category', flat=True).distinct()
        category_list = list(categories)
        
        return Response({
            "status": True,
            "message": "Categories retrieved successfully",
            "data": category_list
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            "status": False,
            "message": f"Error retrieving categories: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_interview_question(request):
  
    try:
        # Validate required fields
        required_fields = ['category', 'question', 'expected_answer', 'keywords']
        for field in required_fields:
            if field not in request.data:
                return Response({
                    "status": False,
                    "message": f"Missing required field: {field}"
                }, status=status.HTTP_400_BAD_REQUEST)

        serializer = InterviewQuestionSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Interview question created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": False,
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            "status": False,
            "message": f"Error creating question: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_questions_by_category(request, category):
    try:
        questions = InterviewQuestion.filter_by_category(category).order_by('created_at')
        
        if not questions.exists():
            return Response({
                "status": False,
                "message": f"No questions found for category: {category}"
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = InterviewQuestionListSerializer(questions, many=True)
        return Response({
            "status": True,
            "message": f"Questions retrieved successfully for category: {category}",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            "status": False,
            "message": f"Error retrieving questions: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_random_question(request):
   
    try:
        from django.db.models import Count
        
        # Get random question from database
        question = InterviewQuestion.objects.order_by('?').first()
        
        if not question:
            return Response({
                "status": False,
                "message": "No questions available"
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = InterviewQuestionListSerializer(question)
        return Response({
            "status": True,
            "message": "Random question retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            "status": False,
            "message": f"Error retrieving question: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def check_answer(request):
   
   
   
    try:
        # Validate required fields
        question_id = request.data.get('question_id')
        user_answer = request.data.get('answer')
        
        if not question_id or not user_answer:
            return Response({
                "status": False,
                "message": "Missing required fields: question_id and answer"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch the question
        try:
            question = InterviewQuestion.objects.get(id=question_id)
        except InterviewQuestion.DoesNotExist:
            return Response({
                "status": False,
                "message": f"Question with id {question_id} not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Convert answer to lowercase for matching
        answer_lower = user_answer.lower()
        
        # Split keywords and calculate score
        keywords = [kw.strip().lower() for kw in question.keywords.split(',')]
        matched_keywords = []
        score = 0
        
        for keyword in keywords:
            if keyword and keyword in answer_lower:
                matched_keywords.append(keyword)
                score += 2  # 2 points for each matched keyword
        
        # Save the answer
        interview_answer = InterviewAnswer.objects.create(
            question=question,
            user_answer=user_answer,
            score=score
        )
        
        return Response({
            "status": True,
            "score": score,
            "matched_keywords": matched_keywords,
            "total_keywords": len(keywords),
            "message": "Answer checked successfully",
            "data": {
                "answer_id": interview_answer.id,
                "question_id": question_id,
                "score": score,
                "matched_count": len(matched_keywords)
            }
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            "status": False,
            "message": f"Error checking answer: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)