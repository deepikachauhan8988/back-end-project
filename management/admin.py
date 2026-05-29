from django.contrib import admin
from .models import Employee, InterviewQuestion, InterviewAnswer


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'role']
    search_fields = ['name', 'email']
    list_filter = ['role']


@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'question', 'created_at']
    search_fields = ['category', 'question']
    list_filter = ['category', 'created_at']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Question Details', {
            'fields': ('category', 'question', 'expected_answer', 'keywords')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )


@admin.register(InterviewAnswer)
class InterviewAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'score', 'created_at']
    search_fields = ['question__question', 'user_answer']
    list_filter = ['score', 'created_at', 'question__category']
    readonly_fields = ['created_at', 'score']
    fieldsets = (
        ('Answer Details', {
            'fields': ('question', 'user_answer', 'score')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )

