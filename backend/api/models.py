from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    def __str__(self) -> str:
        return self.title
    
class Submission(models.Model):
    fileName = models.CharField(max_length=100)
    task = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    username = models.CharField(max_length=100)
    score = models.JSONField()

    def __str__(self) -> str:
        return self.fileName