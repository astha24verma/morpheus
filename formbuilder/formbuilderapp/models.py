from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User
import json

class Form(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPES = [
        ('text', 'Text'),
        ('dropdown', 'Dropdown'),
        ('checkbox', 'Checkbox'),
    ]

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    order = models.IntegerField(validators=[MinValueValidator(1)])
    options = models.JSONField(null=True, blank=True)  # For dropdown and checkbox options

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.form.title} - {self.question_text}"

class Response(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='responses')
    submitted_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True)

class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()  # Stores text for text questions and JSON for others

    def get_answer_value(self):
        if self.question.question_type in ['dropdown', 'checkbox']:
            return json.loads(self.answer_text)
        return self.answer_text
