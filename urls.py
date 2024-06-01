# posts/urls.py
from django.urls import path
from .views import PostCreateView, PostDeleteView, PostDetailView, PostListView, PostUpdateView, DraftPostListView

urlpatterns = [
    path("", PostListView.as_view(), name="list"),
    path("drafts/", DraftPostListView.as_view(), name="drafts"),
    path("<int:pk>/", PostDetailView.as_view(), name="detail"),
    path("new/", PostCreateView.as_view(), name="new"),
    path("<int:pk>/edit/", PostUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="delete"),
]
