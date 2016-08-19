from django.contrib import admin

from .models import Question, Choice, Voter

#registering custom models
admin.site.register(Question)

admin.site.register(Choice)

admin.site.register(Voter)