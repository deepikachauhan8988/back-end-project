# models.py

from django.db import models
from django.contrib.auth.hashers import make_password

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

    department = models.CharField(max_length=50)
    joining_date = models.DateField()
    address = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)

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