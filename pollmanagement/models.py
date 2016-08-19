from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#Poll / Question mode
class Question(models.Model):
    question_text = models.CharField(max_length=300)
    pub_date = models.DateTimeField('date published')
    def __str__(self):              # __unicode__ on Python 2
        return self.question_text

#Choice model
class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=60)
    votes = models.IntegerField(default=0)
    def __str__(self):              # __unicode__ on Python 2
        return self.choice_text

# Vote model to track what all questions / poll user has voted already
class Voter(models.Model):
    user = models.ForeignKey(User)
    poll = models.ForeignKey(Question)