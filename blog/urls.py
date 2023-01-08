from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    # path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/new/', upload, name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('user/<int:pk>/', UserPostListlView.as_view(), name='user-list'),
    path('about/', views.about, name='blog-about'),
    # path('commet/<int:pk>/', views.commet, name='commet'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
