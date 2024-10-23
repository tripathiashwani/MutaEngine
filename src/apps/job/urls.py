from django.urls import path

from .views import (
    OfferLetterTemplateViewSet,
    JobAssignmentTemplateViewSet,
    JobApplicantTemplateViewSet,
    JobTemplateCreateView,
    JobTemplateUpdateView,
    JobTemplateListView,
    JobTemplateRetrieveView,
    JobTemplateDeleteView,
)

urlpatterns = [
    path(
        "offer/letter/", 
        OfferLetterTemplateViewSet.as_view({"get": "list", "post": "create"}), 
        name="offer-letter-template-list"
    ),
    path(
        "offer/letter/<uuid:pk>/", 
        OfferLetterTemplateViewSet.as_view({"get": "retrieve", "patch": "update", "put": "update", "delete": "destroy"}), 
        name="offer-letter-template-detail"
    ),
    path(
        "assignment/template/", 
        JobAssignmentTemplateViewSet.as_view({"get": "list", "post": "create"}), 
        name="job-assignment-template"
    ),
    path(
        "assignment/template/<uuid:pk>/", 
        JobAssignmentTemplateViewSet.as_view({"get": "retrieve", "patch": "update", "put": "update", "delete": "destroy"}), 
        name="job-assignment-template-detail"
    ),
    path(
        "applicant/template/", 
        JobApplicantTemplateViewSet.as_view({"get": "list", "post": "create"}), 
        name="job-applicant-template"
    ),
    path(
        "applicant/template/<uuid:pk>/", 
        JobApplicantTemplateViewSet.as_view({"get": "retrieve", "patch": "update", "put": "update", "delete": "destroy"}), 
        name="job-applicant-template-detail"
    ),
    path("create/", JobTemplateCreateView.as_view(), name="job-template-create"),
    path("<uuid:pk>/update/", JobTemplateUpdateView.as_view(), name="job-template-update"),
    path("list/", JobTemplateListView.as_view(), name="job-template-list"),
    path("<uuid:pk>/", JobTemplateRetrieveView.as_view(), name="job-template-retrieve"),
    path("<uuid:pk>/delete/", JobTemplateDeleteView.as_view(), name="job-template-delete"),
]