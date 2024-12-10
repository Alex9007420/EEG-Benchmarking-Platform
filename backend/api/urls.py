from django.urls import path
from . import views

urlpatterns = [
    path("notes/", views.NoteListCreate.as_view(), name="note-list"),
    path("notes/delete/<int:pk>/", views.NoteDelete.as_view(), name="delete-note"),
    path("submissions/", views.UserSubmissionsViewSet.as_view(), name="user-submissions"),
    path("submission/delete/<int:pk>/", views.SubmissionDelete.as_view(), name="delete-submission"),
    path("submissions/create/", views.createSubmission, name="create-submission"),
    path("submissions/all/", views.SubmissionsViewSet.as_view(), name="all-submissions-list"),
    path("visualize/", views.visualizeSubmission, name="visualize-submission")
]