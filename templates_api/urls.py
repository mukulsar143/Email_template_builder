from django.urls import path
from .views import GetEmailLayoutView, UploadImageView, UploadEmailConfigView, RenderAndDownloadTemplateView

urlpatterns = [
    path('getEmailLayout/', GetEmailLayoutView.as_view()),
    path('uploadImage/', UploadImageView.as_view()),
    path('uploadEmailConfig/', UploadEmailConfigView.as_view()),
    path('renderAndDownloadTemplate/', RenderAndDownloadTemplateView.as_view()),
]
