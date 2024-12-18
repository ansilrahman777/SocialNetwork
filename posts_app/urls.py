from django.urls import path
from .views import HeadshotViewSet, PostViewSet

urlpatterns = [
    path('profile/posts/create/', PostViewSet.as_view({'post': 'create'}), name='post-create'),
    
    path('profile/<int:user_id>/posts/images/', PostViewSet.as_view({'get': 'list_images'}), name='user-post-images'),
    path('profile/<int:user_id>/posts/videos/', PostViewSet.as_view({'get': 'list_videos'}), name='user-post-videos'),
    
    path('profile/posts/<int:pk>/delete/', PostViewSet.as_view({'delete': 'delete_post'}), name='post-delete'),
    path('profile/posts/deleted/', PostViewSet.as_view({'get': 'list_deleted_posts'}), name='deleted-posts'),
    path('profile/posts/<int:pk>/restore/', PostViewSet.as_view({'post': 'restore_post'}), name='post-restore'),
    
    path('profile/posts/<int:pk>/like/', PostViewSet.as_view({'post': 'like'}), name='post-like'),
    path('profile/posts/<int:pk>/unlike/', PostViewSet.as_view({'delete': 'unlike'}), name='post-unlike'),
    path('profile/posts/<int:pk>/comment/', PostViewSet.as_view({'post': 'comment'}), name='post-comment'),
    path('profile/posts/<int:pk>/comment/<int:comment_id>/', PostViewSet.as_view({'delete': 'delete_comment'}), name='post-delete-comment'),
    
    path('profile/posts/<int:pk>/comments/', PostViewSet.as_view({'get': 'list_comments'}), name='post-list-comments'),
    path('profile/posts/<int:pk>/likes/', PostViewSet.as_view({'get': 'list_likes'}), name='post-list-likes'),
    
    path('profile/posts/<int:pk>/', PostViewSet.as_view({'get': 'retrieve'}), name='post-detail'),
    path('profile/posts/<int:pk>/share/', PostViewSet.as_view({'get': 'share'}), name='post-share'),
        
    path('profile/headshots/create/', HeadshotViewSet.as_view({'post': 'create'}), name='headshot-create'),
    path('profile/headshots/<int:pk>/', HeadshotViewSet.as_view({'get': 'retrieve'}), name='headshot-detail'),
    path('profile/<int:user_id>/headshots/', HeadshotViewSet.as_view({'get': 'list_user_headshots'}), name='user-headshots'),
]
