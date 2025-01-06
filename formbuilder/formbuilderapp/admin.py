from django.contrib import admin
from .models import Answer, Form, Question, Response  

admin.site.register(Form)
admin.site.register(Question)
admin.site.register(Response)
admin.site.register(Answer)