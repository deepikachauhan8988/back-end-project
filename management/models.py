# models.py

from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone

class Employee(models.Model):

    # Role Choices
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    # Password Field
    password = models.CharField(max_length=255, blank=True, null=True)

    # Role Field
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='employee'
    )

    regi_id = models.CharField(max_length=20, blank=True, null=True, unique=True)

    class Meta:
        db_table = "management_employee"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        # Generate Registration ID
        if not self.regi_id:
            last_employee = Employee.objects.order_by('-id').first()

            if last_employee:
                new_id_number = last_employee.id + 1
            else:
                new_id_number = 1

            self.regi_id = f"EMP_REGI_{new_id_number:03d}"

        # Encrypt Password
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)


class InterviewQuestion(models.Model):
    """
    Model for storing interview questions with keywords for answer verification
    """
    category = models.CharField(max_length=100)
    question = models.TextField()
    expected_answer = models.TextField()
    keywords = models.TextField(help_text="Comma-separated keywords for answer matching")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "management_interview_question"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.category} - {self.question[:50]}"


class InterviewAnswer(models.Model):
    """
    Model for storing user answers to interview questions with scores
    """
    question = models.ForeignKey(InterviewQuestion, on_delete=models.CASCADE, related_name='answers')
    user_answer = models.TextField()
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "management_interview_answer"
        ordering = ['-created_at']

    def __str__(self):
        return f"Answer to {self.question.category} - Score: {self.score}"