from django.urls import path
from .views import SavedApprenticeshipViewSet, SavedCastingCallViewSet, SavedEventViewSet, SavedGigWorkViewSet, SavedInternshipViewSet, SavedPostViewSet, SavedArtistViewSet, SavedProjectViewSet

urlpatterns = [
    path('artists/save/<int:artist_id>/', SavedArtistViewSet.as_view({'post': 'create'}), name='artist-save'),
    path('artists/unsave/<int:artist_id>/', SavedArtistViewSet.as_view({'delete': 'destroy'}), name='artist-unsave'),
    path('profile/artists/saved/list/', SavedArtistViewSet.as_view({'get': 'list_saved_artists'}), name='saved-artists-list'),
    
    path('post/save/<int:post_id>/', SavedPostViewSet.as_view({'post': 'create'}), name='post-save'),
    path('post/unsave/<int:post_id>/', SavedPostViewSet.as_view({'delete': 'destroy'}), name='post-unsave'),
    path('profile/post/saved/list/', SavedPostViewSet.as_view({'get': 'list_saved_posts'}), name='list-saved-posts'),
    
    path('projects/save/<int:project_id>/', SavedProjectViewSet.as_view({'post': 'create'}), name='project-save'),
    path('projects/unsave/<int:project_id>/', SavedProjectViewSet.as_view({'delete': 'destroy'}), name='project-unsave'),
    path('profile/projects/saved/list/', SavedProjectViewSet.as_view({'get': 'list_saved_projects'}), name='saved-projects-list'),
    
    path('gigs/save/<int:gig_id>/', SavedGigWorkViewSet.as_view({'post': 'create'}), name='gig-save'),
    path('gigs/unsave/<int:gig_id>/', SavedGigWorkViewSet.as_view({'delete': 'destroy'}), name='gig-unsave'),
    path('profile/gigs/saved/list/', SavedGigWorkViewSet.as_view({'get': 'list_saved_gigs'}), name='saved-gigs-list'),
    
    path('casting_calls/save/<int:casting_call_id>/', SavedCastingCallViewSet.as_view({'post': 'create'}), name='casting-call-save'),
    path('casting_calls/unsave/<int:casting_call_id>/', SavedCastingCallViewSet.as_view({'delete': 'destroy'}), name='casting-call-unsave'),
    path('profile/casting_calls/saved/list/', SavedCastingCallViewSet.as_view({'get': 'list_saved_casting_calls'}), name='saved-casting-calls-list'),
    
    path('events/save/<int:event_id>/', SavedEventViewSet.as_view({'post': 'create'}), name='event-save'),
    path('events/unsave/<int:event_id>/', SavedEventViewSet.as_view({'delete': 'destroy'}), name='event-unsave'),
    path('profile/events/saved/list/', SavedEventViewSet.as_view({'get': 'list_saved_events'}), name='saved-events-list'),
    
    path('internships/save/<int:internship_id>/', SavedInternshipViewSet.as_view({'post': 'create'}), name='internship-save'),
    path('internships/unsave/<int:internship_id>/', SavedInternshipViewSet.as_view({'delete': 'destroy'}), name='internship-unsave'),
    path('profile/internships/saved/list/', SavedInternshipViewSet.as_view({'get': 'list_saved_internships'}), name='saved-internships-list'),
    
    path('apprenticeships/save/<int:apprenticeship_id>/', SavedApprenticeshipViewSet.as_view({'post': 'create'}), name='apprenticeship-save'),
    path('apprenticeships/unsave/<int:apprenticeship_id>/', SavedApprenticeshipViewSet.as_view({'delete': 'destroy'}), name='apprenticeship-unsave'),
    path('profile/apprenticeships/saved/list/', SavedApprenticeshipViewSet.as_view({'get': 'list_saved_apprenticeships'}), name='saved-apprenticeships-list'),
]
