from django.urls import path

from .views import JobApplicantViewSet, AssignmentSubmissionViewSet, SubmitSignedOfferLetterView, TilesDataView, TemplateTestView


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
    path(
        "submit/signed/offer/letter/",
        SubmitSignedOfferLetterView.as_view(),
        name="submit-signed-offer-letter-view"
    ),
    path("tiles/", TilesDataView.as_view(), name="tiles-data-view"),
    path("test/template/", TemplateTestView.as_view(), name="template-test")
]