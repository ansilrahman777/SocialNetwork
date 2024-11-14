from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .serializers import SavedApprenticeshipSerializer, SavedCastingCallSerializer, SavedEventSerializer, SavedGigWorkSerializer, SavedInternshipSerializer, SavedPostSerializer, SavedArtistSerializer, SavedProjectSerializer
from .models import SavedApprenticeship, SavedCastingCall, SavedEvent, SavedGigWork, SavedInternship, SavedPost, SavedArtist, SavedProject
from posts_app.models import Post
from userprofile_app.models import Profile
from forms.models import Project, GigWork, CastingCall, EventDetails, Internship, Apprenticeship


class SavedArtistViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, artist_id=None):
        """Save an artist profile."""
        try:
            artist_profile = Profile.objects.get(user_id=artist_id)
        except Profile.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Artist does not exist."
            }, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        saved_artist, created = SavedArtist.objects.get_or_create(user=user, artist_profile=artist_profile)
        if not created:
            return Response({
                "status": "error",
                "message": "Artist is already saved."
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": "success",
            "message": "Artist saved successfully",
            "savedArtist": {
                "artistId": artist_profile.user.id,
                "savedAt": saved_artist.saved_at
            }
        }, status=status.HTTP_201_CREATED)

    def destroy(self, request, artist_id=None):
        """Unsave an artist profile."""
        saved_artist = SavedArtist.objects.filter(user=request.user, artist_profile__user_id=artist_id).first()
        if saved_artist:
            saved_artist.delete()
            return Response({
                "status": "success",
                "message": "Artist unsaved successfully",
                "unsavedArtist": {
                    "artistId": artist_id,
                    "unsavedAt": timezone.now()
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": "Artist not found in saved list."
        }, status=status.HTTP_404_NOT_FOUND)

    def list_saved_artists(self, request):
        """List all saved artist profiles for the user."""
        saved_artists = SavedArtist.objects.filter(user=request.user)
        if not saved_artists.exists():
            return Response({
                "status": "error",
                "message": "No saved artists found."
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SavedArtistSerializer(saved_artists, many=True)
        return Response({
            "status": "success",
            "data": {
                "totalArtists": saved_artists.count(),
                "artists": serializer.data
            }
        }, status=status.HTTP_200_OK)

class SavedPostViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, post_id=None):
        if not Post.objects.filter(id=post_id).exists():
            return Response({
                "status": "error",
                "message": "Post does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        
        user = request.user
        saved_post, created = SavedPost.objects.get_or_create(user=user, post_id=post_id)
        if not created:
            return Response({
                "status": "error",
                "message": "Post is already saved."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "status": "success",
            "message": "Post saved successfully",
            "savedPost": {
                "postId": saved_post.post.id,
                "savedAt": saved_post.saved_at
            }
        }, status=status.HTTP_201_CREATED)

    def destroy(self, request, post_id=None):
        saved_post = SavedPost.objects.filter(user=request.user, post_id=post_id).first()
        if saved_post:
            saved_post.delete()
            return Response({
                "status": "success",
                "message": "Post unsaved successfully",
                "unsavedPost": {
                    "postId": post_id,
                    "unsavedAt": timezone.now()
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": "Post not found in saved list."
        }, status=status.HTTP_404_NOT_FOUND)

    def list_saved_posts(self, request):
        saved_posts = SavedPost.objects.filter(user=request.user)
        if not saved_posts.exists():
            return Response({
                "status": "error",
                "message": "No saved posts found for this user."
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = SavedPostSerializer(saved_posts, many=True)
        return Response({
            "status": "success",
            "savedPosts": serializer.data
        }, status=status.HTTP_200_OK)

class SavedProjectViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, project_id=None):
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Project does not exist."
            }, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        saved_project, created = SavedProject.objects.get_or_create(user=user, project=project)
        if not created:
            return Response({
                "status": "error",
                "message": "Project is already saved."
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": "success",
            "message": "Project saved successfully",
            "savedProject": {
                "projectId": project.id,
                "savedAt": saved_project.saved_at
            }
        }, status=status.HTTP_201_CREATED)

    def destroy(self, request, project_id=None):
        saved_project = SavedProject.objects.filter(user=request.user, project_id=project_id).first()
        if saved_project:
            saved_project.delete()
            return Response({
                "status": "success",
                "message": "Project unsaved successfully",
                "unsavedProject": {
                    "projectId": project_id,
                    "unsavedAt": timezone.now()
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": "Project not found in saved list."
        }, status=status.HTTP_404_NOT_FOUND)

    def list_saved_projects(self, request):
        saved_projects = SavedProject.objects.filter(user=request.user)
        if not saved_projects.exists():
            return Response({
                "status": "error",
                "message": "No saved projects found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = SavedProjectSerializer(saved_projects, many=True)
        return Response({
            "status": "success",
            "data": {
                "totalProjects": saved_projects.count(),
                "projects": serializer.data
            }
        }, status=status.HTTP_200_OK)

class SavedGigWorkViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, gig_id=None):
        try:
            gig_work = GigWork.objects.get(id=gig_id)
        except GigWork.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Gig does not exist."
            }, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        saved_gig, created = SavedGigWork.objects.get_or_create(user=user, gig_work=gig_work)
        if not created:
            return Response({
                "status": "error",
                "message": "Gig is already saved."
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": "success",
            "message": "Gig saved successfully",
            "savedGig": {
                "gigId": gig_work.id,
                "savedAt": saved_gig.saved_at
            }
        }, status=status.HTTP_201_CREATED)

    def destroy(self, request, gig_id=None):
        saved_gig = SavedGigWork.objects.filter(user=request.user, gig_work_id=gig_id).first()
        if saved_gig:
            saved_gig.delete()
            return Response({
                "status": "success",
                "message": "Gig unsaved successfully",
                "unsavedGig": {
                    "gigId": gig_id,
                    "unsavedAt": timezone.now()
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": "Gig not found in saved list."
        }, status=status.HTTP_404_NOT_FOUND)

    def list_saved_gigs(self, request):
        saved_gigs = SavedGigWork.objects.filter(user=request.user)
        if not saved_gigs.exists():
            return Response({
                "status": "error",
                "message": "No saved gigs found."
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SavedGigWorkSerializer(saved_gigs, many=True)
        return Response({
            "status": "success",
            "data": {
                "totalGigs": saved_gigs.count(),
                "gigs": serializer.data
            }
        }, status=status.HTTP_200_OK)
        
class SavedCastingCallViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, casting_call_id=None):
        try:
            casting_call = CastingCall.objects.get(id=casting_call_id)
        except CastingCall.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Casting call does not exist."
            }, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        saved_casting, created = SavedCastingCall.objects.get_or_create(user=user, casting_call=casting_call)
        if not created:
            return Response({
                "status": "error",
                "message": "Casting call is already saved."
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": "success",
            "message": "Casting call saved successfully",
            "savedCastingCall": {
                "castingCallId": casting_call.id,
                "savedAt": saved_casting.saved_at
            }
        }, status=status.HTTP_201_CREATED)

    def destroy(self, request, casting_call_id=None):
        saved_casting = SavedCastingCall.objects.filter(user=request.user, casting_call_id=casting_call_id).first()
        if saved_casting:
            saved_casting.delete()
            return Response({
                "status": "success",
                "message": "Casting call unsaved successfully",
                "unsavedCastingCall": {
                    "castingCallId": casting_call_id,
                    "unsavedAt": timezone.now()
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": "Casting call not found in saved list."
        }, status=status.HTTP_404_NOT_FOUND)

    def list_saved_casting_calls(self, request):
        saved_casting_calls = SavedCastingCall.objects.filter(user=request.user)
        if not saved_casting_calls.exists():
            return Response({
                "status": "error",
                "message": "No saved casting calls found."
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SavedCastingCallSerializer(saved_casting_calls, many=True)
        return Response({
            "status": "success",
            "data": {
                "totalCastingCalls": saved_casting_calls.count(),
                "castingCalls": serializer.data
            }
        }, status=status.HTTP_200_OK)
        
class SavedEventViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, event_id=None):
        try:
            event = EventDetails.objects.get(id=event_id)
        except EventDetails.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Event does not exist."
            }, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        saved_event, created = SavedEvent.objects.get_or_create(user=user, event=event)
        if not created:
            return Response({
                "status": "error",
                "message": "Event is already saved."
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": "success",
            "message": "Event saved successfully",
            "savedEvent": {
                "eventId": event.id,
                "savedAt": saved_event.saved_at
            }
        }, status=status.HTTP_201_CREATED)

    def destroy(self, request, event_id=None):
        saved_event = SavedEvent.objects.filter(user=request.user, event_id=event_id).first()
        if saved_event:
            saved_event.delete()
            return Response({
                "status": "success",
                "message": "Event unsaved successfully",
                "unsavedEvent": {
                    "eventId": event_id,
                    "unsavedAt": timezone.now()
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": "Event not found in saved list."
        }, status=status.HTTP_404_NOT_FOUND)

    def list_saved_events(self, request):
        saved_events = SavedEvent.objects.filter(user=request.user)
        if not saved_events.exists():
            return Response({
                "status": "error",
                "message": "No saved events found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = SavedEventSerializer(saved_events, many=True)
        return Response({
            "status": "success",
            "data": {
                "totalEvents": saved_events.count(),
                "events": serializer.data
            }
        }, status=status.HTTP_200_OK)
        
class SavedInternshipViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, internship_id=None):
        try:
            internship = Internship.objects.get(id=internship_id)
        except Internship.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Internship does not exist."
            }, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        saved_internship, created = SavedInternship.objects.get_or_create(user=user, internship=internship)
        if not created:
            return Response({
                "status": "error",
                "message": "Internship is already saved."
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": "success",
            "message": "Internship saved successfully",
            "savedInternship": {
                "internshipId": internship.id,
                "savedAt": saved_internship.saved_at
            }
        }, status=status.HTTP_201_CREATED)

    def destroy(self, request, internship_id=None):
        saved_internship = SavedInternship.objects.filter(user=request.user, internship_id=internship_id).first()
        if saved_internship:
            saved_internship.delete()
            return Response({
                "status": "success",
                "message": "Internship unsaved successfully",
                "unsavedInternship": {
                    "internshipId": internship_id,
                    "unsavedAt": timezone.now()
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": "Internship not found in saved list."
        }, status=status.HTTP_404_NOT_FOUND)

    def list_saved_internships(self, request):
        saved_internships = SavedInternship.objects.filter(user=request.user)
        if not saved_internships.exists():
            return Response({
                "status": "error",
                "message": "No saved internships found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = SavedInternshipSerializer(saved_internships, many=True)
        return Response({
            "status": "success",
            "data": {
                "totalInternships": saved_internships.count(),
                "internships": serializer.data
            }
        }, status=status.HTTP_200_OK)
        
class SavedApprenticeshipViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, apprenticeship_id=None):
        try:
            apprenticeship = Apprenticeship.objects.get(id=apprenticeship_id)
        except Apprenticeship.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Apprenticeship does not exist."
            }, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        saved_apprenticeship, created = SavedApprenticeship.objects.get_or_create(user=user, apprenticeship=apprenticeship)
        if not created:
            return Response({
                "status": "error",
                "message": "Apprenticeship is already saved."
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": "success",
            "message": "Apprenticeship saved successfully",
            "savedApprenticeship": {
                "apprenticeshipId": apprenticeship.id,
                "savedAt": saved_apprenticeship.saved_at
            }
        }, status=status.HTTP_201_CREATED)

    def destroy(self, request, apprenticeship_id=None):
        saved_apprenticeship = SavedApprenticeship.objects.filter(user=request.user, apprenticeship_id=apprenticeship_id).first()
        if saved_apprenticeship:
            saved_apprenticeship.delete()
            return Response({
                "status": "success",
                "message": "Apprenticeship unsaved successfully",
                "unsavedApprenticeship": {
                    "apprenticeshipId": apprenticeship_id,
                    "unsavedAt": timezone.now()
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": "Apprenticeship not found in saved list."
        }, status=status.HTTP_404_NOT_FOUND)

    def list_saved_apprenticeships(self, request):
        saved_apprenticeships = SavedApprenticeship.objects.filter(user=request.user)
        if not saved_apprenticeships.exists():
            return Response({
                "status": "error",
                "message": "No saved apprenticeships found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = SavedApprenticeshipSerializer(saved_apprenticeships, many=True)
        return Response({
            "status": "success",
            "data": {
                "totalApprenticeships": saved_apprenticeships.count(),
                "apprenticeships": serializer.data
            }
        }, status=status.HTTP_200_OK)       
