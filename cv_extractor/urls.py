from django.urls import path
from .views import CvExtractorView


urlpatterns = [
    path(
        "",
        CvExtractorView.as_view(
            {"post": "post"},
        ),
    ),
]
