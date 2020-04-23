from django.db import models

class Student(models.Model):
    user_name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    message = models.TextField()
    group = models.IntegerField(default=0)