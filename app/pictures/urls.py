from django.urls import path
from .views import (
    PictureAdminApiView,
    PictureListApiView,
    PictureDetailApiView
)

urlpatterns = [
    path('picture', PictureListApiView.as_view(), name="picture-list"),
    path('picture/<int:picture_id>', PictureDetailApiView.as_view(), name="picture-detail"),
    path('picture/purge', PictureAdminApiView.as_view(), name="picture-detail"),
]