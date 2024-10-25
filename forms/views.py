from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from .models import PostFeed,GigWork,CastingCall,Project
from .serializers import GigWorkSerializer, CastingCallSerializer, ProjectSerializer, PostFeedSerializer
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from .models import EventRegistration, Internship, Apprenticeship
from rest_framework.authentication import TokenAuthentication
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
    
    def get(self, request, pk=None):
        if pk:
            try:
                gig_work = GigWork.objects.get(pk=pk)
                serializer = GigWorkSerializer(gig_work)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            except GigWork.DoesNotExist:
                return Response({"message": "Gig work not found."}, status=status.HTTP_404_NOT_FOUND)
        
        gig_works = GigWork.objects.all()
        serializer = GigWorkSerializer(gig_works, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            gig_work = GigWork.objects.get(pk=pk)
            serializer = GigWorkSerializer(gig_work, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Gig work updated successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except GigWork.DoesNotExist:
            return Response({"message": "Gig work not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            gig_work = GigWork.objects.get(pk=pk)
            gig_work.delete()
            return Response({"message": "Gig work deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except GigWork.DoesNotExist:
            return Response({"message": "Gig work not found."}, status=status.HTTP_404_NOT_FOUND)

    
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

    def get(self, request, pk=None):
        if pk:
            try:
                casting_call = CastingCall.objects.get(pk=pk)
                serializer = CastingCallSerializer(casting_call)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            except CastingCall.DoesNotExist:
                return Response({"message": "Casting call not found."}, status=status.HTTP_404_NOT_FOUND)
        
        casting_calls = CastingCall.objects.all()
        serializer = CastingCallSerializer(casting_calls, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            casting_call = CastingCall.objects.get(pk=pk)
            serializer = CastingCallSerializer(casting_call, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Casting call updated successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CastingCall.DoesNotExist:
            return Response({"message": "Casting call not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            casting_call = CastingCall.objects.get(pk=pk)
            casting_call.delete()
            return Response({"message": "Casting call deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except CastingCall.DoesNotExist:
            return Response({"message": "Casting call not found."}, status=status.HTTP_404_NOT_FOUND)


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

    def get(self, request, pk=None):
        if pk:
            try:
                project = Project.objects.get(pk=pk)
                serializer = ProjectSerializer(project)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            except Project.DoesNotExist:
                return Response({"message": "Project not found."}, status=status.HTTP_404_NOT_FOUND)
        
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            serializer = ProjectSerializer(project, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Project updated successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response({"message": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            project.delete()
            return Response({"message": "Project deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({"message": "Project not found."}, status=status.HTTP_404_NOT_FOUND)



class PostFeedView(generics.CreateAPIView):
    queryset = PostFeed.objects.all()
    serializer_class = PostFeedSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]  # Ensure TokenAuthentication is used
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


    def get(self, request, pk=None):
        if pk:
            try:
                post = PostFeed.objects.get(pk=pk)
                serializer = PostFeedSerializer(post)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            except PostFeed.DoesNotExist:
                return Response({"message": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        posts = PostFeed.objects.all()
        serializer = PostFeedSerializer(posts, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            post = PostFeed.objects.get(pk=pk)
            serializer = PostFeedSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Post updated successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PostFeed.DoesNotExist:
            return Response({"message": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            post = PostFeed.objects.get(pk=pk)
            post.delete()
            return Response({"message": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except PostFeed.DoesNotExist:
            return Response({"message": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

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
    

    def get(self, request, user_id=None):
        if user_id:
            try:
                internship = Internship.objects.get(user_id=user_id)
                serializer = InternshipSerializer(internship)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            except Internship.DoesNotExist:
                return Response({"message": "Internship not found."}, status=status.HTTP_404_NOT_FOUND)
        
        internships = Internship.objects.all()
        serializer = InternshipSerializer(internships, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        try:
            internship = Internship.objects.get(user_id=user_id)
            serializer = InternshipSerializer(internship, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Internship updated successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Internship.DoesNotExist:
            return Response({"message": "Internship not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_id):
        try:
            internship = Internship.objects.get(user_id=user_id)
            internship.delete()
            return Response({"message": "Internship deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Internship.DoesNotExist:
            return Response({"message": "Internship not found."}, status=status.HTTP_404_NOT_FOUND)


# ----------------------------
# Event Registration View
# ----------------------------

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

class EventRegistrationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=EventRegistrationSerializer)
    def post(self, request):
        serializer = EventRegistrationSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            event_registration = serializer.save()  # Calls the create method of the serializer
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

    def get(self, request, user_id):
        if user_id:
            try:
            # Use the primary key (pk) to fetch the event registration
                event_registration = EventRegistration.objects.get(user_id=user_id)
                serializer = EventRegistrationSerializer(event_registration)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            except EventRegistration.DoesNotExist:
                return Response({"message": "Event registration not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, user_id):
        try:
            event_registration = EventRegistration.objects.get(user_id=user_id)
            serializer = EventRegistrationSerializer(event_registration, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Event registration updated successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except EventRegistration.DoesNotExist:
            return Response({"message": "Event registration not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_id):
        try:
            event_registration = EventRegistration.objects.get(user_id=user_id)
            event_registration.delete()
            return Response({"message": "Event registration deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except EventRegistration.DoesNotExist:
            return Response({"message": "Event registration not found."}, status=status.HTTP_404_NOT_FOUND)


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
    

    def get(self, request, user_id=None):
        if user_id:
            try:
                apprenticeship = Apprenticeship.objects.get(user_id=user_id)
                serializer = ApprenticeshipSerializer(apprenticeship)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            except Apprenticeship.DoesNotExist:
                return Response({"message": "Apprenticeship not found."}, status=status.HTTP_404_NOT_FOUND)

        apprenticeships = Apprenticeship.objects.all()
        serializer = ApprenticeshipSerializer(apprenticeships, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        try:
            apprenticeship = Apprenticeship.objects.get(user_id=user_id)
            serializer = ApprenticeshipSerializer(apprenticeship, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Apprenticeship updated successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Apprenticeship.DoesNotExist:
            return Response({"message": "Apprenticeship not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_id):
        try:
            apprenticeship = Apprenticeship.objects.get(user_id=user_id)
            apprenticeship.delete()
            return Response({"message": "Apprenticeship deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Apprenticeship.DoesNotExist:
            return Response({"message": "Apprenticeship not found."}, status=status.HTTP_404_NOT_FOUND)
