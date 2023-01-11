from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    # path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/new/', post_create_view, name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('postimages/<int:pk>/', PostImageListView.as_view(), name='postimages-list'),
    path('postimages/<int:pk>/update', PostImageUpdateView.as_view(), name='postimages-update'),
    path('postimages/<int:pk>/delete', PostImageDeleteView.as_view(), name='postimages-delete'),
    path('postimages/<int:pk>/create', PostImageCreateView.as_view(), name='postimages-create'),
    path('user/<int:pk>/', UserPostListlView.as_view(), name='user-list'),
    path('about/', views.about, name='blog-about'),
    # path('commet/<int:pk>/', views.commet, name='commet'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
