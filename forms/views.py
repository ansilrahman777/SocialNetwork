from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from .models import PostFeed
from .serializers import GigWorkSerializer, CastingCallSerializer, ProjectSerializer, PostFeedSerializer
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from .models import EventRegistration, Internship, Apprenticeship
from .serializers import EventRegistrationSerializer,InternshipSerializer,ApprenticeshipSerializer



CustomUser = get_user_model()

class GigWorkFormView(APIView):
    def post(self, request):
        # Pass the request context to the serializer
        serializer = GigWorkSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            gig_work = serializer.save()
            return Response({
                "status": {
                    "type": "success",
                    "message": "Gig work form submitted successfully",
                    "code": 200,
                    "error": False
                },
                "data": {
                    "form_id": gig_work.id,
                    "submission_status": "received",
                    "gig_title": gig_work.gig_title,
                    "user_id": gig_work.user.id,
                }
            }, status=status.HTTP_200_OK)

        return Response({
            "status": {
                "type": "error",
                "message": "Validation Failed",
                "code": 400,
                "error": True
            },
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
class CastingCallFormView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = CastingCallSerializer(data=request.data, context={'request': request})  # Pass request context
        if serializer.is_valid():
            casting_call = serializer.save()
            return Response({
                "status": {
                    "type": "success",
                    "message": "Casting Call Created Successfully",
                    "code": 200,
                    "error": False
                },
                "data": {
                    "casting_call_id": casting_call.id,
                    "job_title": casting_call.job_title,
                    "project_link": casting_call.project_link,
                    "short_description": casting_call.short_description,
                    "created_at": casting_call.created_at,
                }
            }, status=status.HTTP_200_OK)

        return Response({
            "status": {
                "type": "error",
                "message": "Validation Failed",
                "code": 400,
                "error": True,
                "errors": serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

class ProjectFormView(APIView):
    def post(self, request):
        serializer = ProjectSerializer(data=request.data, context={'request': request})  # Pass request context
        if serializer.is_valid():
            project = serializer.save()
            return Response({
                "status": {
                    "type": "success",
                    "message": "Project Created Successfully",
                    "code": 200,
                    "error": False
                },
                "data": {
                    "project_id": project.id,
                    "project_title": project.project_title,
                    "created_at": project.created_at
                }
            }, status=status.HTTP_200_OK)

        return Response({
            "status": {
                "type": "error",
                "message": "Validation Failed",
                "code": 400,
                "error": True,
                "errors": serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)



class PostFeedView(generics.CreateAPIView):
    queryset = PostFeed.objects.all()
    serializer_class = PostFeedSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        post = serializer.save()  # Automatically associates the post with the logged-in user
        media_url = request.build_absolute_uri(post.media_file.url) if post.media_file else None
        media_type = "video" if post.media_file.name.endswith(('.mp4', '.mov')) else "image"

        return Response({
            "status": {
                "type": "success",
                "message": "Post created successfully",
                "code": 201,
                "error": False
            },
            "data": {
                "post_id": post.id,
                "user_id": post.user.id,
                "media_url": media_url,
                "description": post.description,
                "created_at": post.created_at.isoformat(),
                "submission_status": "Submitted Live or Save as a Draft",
                "media_type": media_type
            }
        }, status=status.HTTP_201_CREATED)


# ----------------------------
# Internship View
# ----------------------------
class InternshipCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=InternshipSerializer)
    def post(self, request):
        serializer = InternshipSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            internship = serializer.save(user=request.user)  # Associate with the authenticated user
            return Response({
                "status": {
                    "type": "success",
                    "message": "Internship application submitted successfully",
                    "code": 201,
                    "error": False
                },
                "data": {
                    "application_id": internship.id,  # Unique identifier for the application
                    "submission_date": internship.start_date.isoformat(),  # Assuming start_date is a DateField
                    "submission_status": "Submitted Live or Save as a Draft"
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": {
                "type": "error",
                "message": "Validation failed",
                "code": 400,
                "error": True,
                "errors": serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------
# Event Registration View
# ----------------------------
class EventRegistrationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=EventRegistrationSerializer)
    def post(self, request):
        serializer = EventRegistrationSerializer(data=request.data, context={'request': request})  # Pass request context

        if serializer.is_valid():
            event_registration = serializer.save()  # Call save without user, as it is set in the serializer
            return Response({
                "status": {
                    "type": "success",
                    "message": "Event registration submitted successfully",
                    "code": 201,
                    "error": False
                },
                "data": {
                    "event_id": event_registration.id,
                    "event_status": "Pending approval",
                    "submission_status": "Submitted"
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": {
                "type": "error",
                "message": "Invalid data",
                "code": 400,
                "error": True,
                "errors": serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------
# Apprenticeship View
# ----------------------------
class ApprenticeshipCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ApprenticeshipSerializer)
    def post(self, request):
        serializer = ApprenticeshipSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            apprenticeship = serializer.save(user=request.user)  # Associate with the authenticated user
            return Response({
                "status": {
                    "type": "success",
                    "message": "Apprenticeship application submitted successfully",
                    "code": 201,
                    "error": False
                },
                "data": {
                    "application_id": apprenticeship.id,  # Unique identifier for the application
                    "submission_date": apprenticeship.start_date.isoformat(),  # Assuming start_date is a DateField
                    "submission_status": "Submitted Live or Save as a Draft"
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": {
                "type": "error",
                "message": "Invalid data",
                "code": 400,
                "error": True,
                "errors": serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)
