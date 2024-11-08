from django.urls import path
from .views import SavedPostViewSet, SavedArtistViewSet

urlpatterns = [
    path('profile/artists/save/<int:artist_id>/', SavedArtistViewSet.as_view({'post': 'create'}), name='artist-save'),
    path('profile/artists/unsave/<int:artist_id>/', SavedArtistViewSet.as_view({'delete': 'destroy'}), name='artist-unsave'),
    path('profile/artists/saved/list/', SavedArtistViewSet.as_view({'get': 'list_saved_artists'}), name='saved-artists-list'),
    
    path('profile/post/save/<int:post_id>/', SavedPostViewSet.as_view({'post': 'create'}), name='post-save'),
    path('profile/post/unsave/<int:post_id>/', SavedPostViewSet.as_view({'delete': 'destroy'}), name='post-unsave'),
    path('profile/post/saved/list/', SavedPostViewSet.as_view({'get': 'list_saved_posts'}), name='list-saved-posts'),
]
