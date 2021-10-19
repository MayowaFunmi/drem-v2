from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Questions(models.Model):
    question = models.TextField()
    option1 = models.CharField(max_length=1000)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.question} ({self.answer})'


class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.user.username} scored {self.score}'