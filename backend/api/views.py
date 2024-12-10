from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserSerializer, NoteSerializer, SubmissionSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Note, Submission
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .utils.submissionFileProccessing import *
from .utils.visualize import *

# Create your views here.
class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)

class NoteDelete(generics.DestroyAPIView):
    serializer_class = Note
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

class SubmissionDelete(generics.DestroyAPIView):
    serializer_class = Submission
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Submission.objects.filter(user=user)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all() #List of All User Objects
    serializer_class = UserSerializer #Which kind of Data we need to accept to create a new User
    permission_classes = [AllowAny] #Who can call this (here: Anyone)

#The @api_view decorator for working with function based views.
@api_view(['GET'])
def getData(request):
    permission_classes = [AllowAny]
    submission = {
        "fileName": "submission 1",
        "task": "LR",
        "uploaded at": None,
        "user": "username1",
        "score": {
            "Overall": 0.5,
            "Hardware1": 0.4,
            "Dots": 0.3
        }
    }
    return Response(submission)

class SubmissionsViewSet(generics.ListAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [AllowAny]

class UserSubmissionsViewSet(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in

    def get_queryset(self):
        # Filter submissions to only those belonging to the authenticated user
        return Submission.objects.filter(user=self.request.user)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createSubmission(request):
    print("TEST")
    uploaded_file = request.FILES.get("file")
    task = request.POST.get("task")

    if not uploaded_file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
    
    file_content = uploaded_file.read().decode('utf-8')  # Read and decode the file content
    contentJSON = json.loads(file_content)

    calculatedScores = process(contentJSON, task)
    
    response_object = {
        "fileName": str(uploaded_file),
        "task": task,
        "uploaded_at": None,
        "user": request.user.id,
        "username": request.user.username,
        "score": calculatedScores,
    }


    serializer = SubmissionSerializer(data=response_object)
    if serializer.is_valid():
        print("VALID REQUEST")
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    print("INVALID REQUEST")
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def visualizeSubmission(request):
    uploaded_file = request.FILES.get("file")
    task = request.POST.get("task")
    file_content = uploaded_file.read().decode('utf-8')  # Read and decode the file content
    contentJSON = json.loads(file_content)

    response_object = getVisualizationData(contentJSON, task)

    return Response(response_object)
