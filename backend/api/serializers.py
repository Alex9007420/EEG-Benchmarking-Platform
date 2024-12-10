from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note, Submission

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}}

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ["id", "fileName", "task", "uploaded_at", "user", "username", "score"]


# fileName = models.CharField(max_length=100)
#     task = models.CharField(max_length=100)
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
#     score = models.JSONField(default=dict)