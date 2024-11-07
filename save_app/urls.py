from django.urls import path
from .views import SavedPostViewSet

urlpatterns = [
    path('profile/post/save/<int:post_id>/', SavedPostViewSet.as_view({'post': 'create'}), name='post-save'),
    path('profile/post/unsave/<int:post_id>/', SavedPostViewSet.as_view({'delete': 'destroy'}), name='post-unsave'),
    path('profile/<int:user_id>/saved_posts/', SavedPostViewSet.as_view({'get': 'list_saved_posts'}), name='list-saved-posts'),
]
