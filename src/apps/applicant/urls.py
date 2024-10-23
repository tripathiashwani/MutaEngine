from django.urls import path

from .views import JobApplicantViewSet, AssignmentSubmissionViewSet


urlpatterns = [
    path("",JobApplicantViewSet.as_view({"get": "list", "post": "create"}), name="applicant-view-set"),
    path("<uuid:pk>/", JobApplicantViewSet.as_view({"get": "retrieve",}), name="applicant-detail-view-set"),
    path(
        "assignment/submission/", 
        AssignmentSubmissionViewSet.as_view({"get": "list", "post": "create"}), 
        name="assignment-submission-view-set"
    ),
    path(
        "assignment/submission/<uuid:pk>/",
        AssignmentSubmissionViewSet.as_view({"get": "retrieve",}), 
        name="assignment-submission-detail-view-set"
    ),
]