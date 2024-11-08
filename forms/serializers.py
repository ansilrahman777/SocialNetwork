import os
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import GigWork, CastingCall, Project
from .models import Internship, Apprenticeship, EventRegistration, BankDetails, Uploads, EventDetails


CustomUser = get_user_model()

class GigWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = GigWork
        fields = ['work_type', 'project_id', 'gig_title', 'short_description', 
                  'work_hours', 'hours_type', 'price', 'price_type', 
                  'skills', 'progress_of_project', 'work_method', 'promotion']

    def create(self, validated_data):
        user = self.context['request'].user  # Get the user from the request
        gig_work = GigWork.objects.create(user=user, **validated_data)
        return gig_work


# Casting Call Serializer
class CastingCallSerializer(serializers.ModelSerializer):
    script_file = serializers.FileField(required=False)

    class Meta:
        model = CastingCall
        fields = ['job_title', 'project_link', 'short_description', 'gender', 
                  'experience', 'role_type', 'age', 'skills', 'height', 
                  'body_type', 'script_file', 'script_url', 'audition_type', 
                  'offline_location', 'casting_call_date', 'casting_call_end_date', 
                  'start_time', 'end_time']

    def create(self, validated_data):
        user = self.context['request'].user  # Get the user from the request
        casting_call = CastingCall.objects.create(user=user, **validated_data)
        return casting_call

# Project Serializer
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_title', 'project_tagline', 'film_name', 'film_role', 
                  'project_status', 'progress_percentage', 'project_type', 'language', 
                  'description', 'primary_email', 'secondary_email', 'team', 
                  'media_files', 'hashtags', 'press_release_link', 
                  'media_release_link', 'social_media_links', 'genre']

    def create(self, validated_data):
        user = self.context['request'].user  # Get the user from the request
        project = Project.objects.create(user=user, **validated_data)
        return project


class BankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetails
        fields = '__all__'

class UploadsSerializer(serializers.ModelSerializer):
    pan_card = serializers.FileField()
    cancelled_cheque = serializers.FileField()

    class Meta:
        model = Uploads
        fields = ['pan_card', 'cancelled_cheque']

    def validate(self, attrs):
        """Ensure uploaded files have valid names and sanitize them."""
        for field_name, file in attrs.items():
            if file:
                # Validate that the file name doesn't contain backslashes or other invalid characters
                if '\\' in file.name:
                    raise serializers.ValidationError(
                        f"File name for {field_name} must not contain '\\'."
                    )
                
                # Sanitize the file name
                sanitized_name = os.path.basename(file.name).replace('\\', '')
                if sanitized_name != file.name:
                    file.name = sanitized_name  # Assign sanitized name back to the file

                # Additional validation for invalid characters (optional)
                invalid_chars = ['/', ':', '*', '?', '"', '<', '>', '|']
                if any(char in sanitized_name for char in invalid_chars):
                    raise serializers.ValidationError(
                        f"File name for {field_name} contains invalid characters: {', '.join(invalid_chars)}."
                    )

        return attrs

class EventDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDetails
        fields = '__all__'

class EventRegistrationSerializer(serializers.ModelSerializer):
    bank_details = BankDetailsSerializer()
    uploads = UploadsSerializer()
    event_details = EventDetailsSerializer()

    class Meta:
        model = EventRegistration
        exclude = ['user']  # Exclude the user field

    def create(self, validated_data):
        request = self.context['request']

        bank_data = validated_data.pop('bank_details')
        uploads_data = validated_data.pop('uploads')
        event_data = validated_data.pop('event_details')

        # Create related instances
        bank_details = BankDetails.objects.create(**bank_data)
        uploads = Uploads.objects.create(**uploads_data)
        event_details = EventDetails.objects.create(**event_data)

        # Create event registration with related data and user
        event_registration = EventRegistration.objects.create(
            user=request.user,
            bank_details=bank_details,
            uploads=uploads,
            event_details=event_details,
            **validated_data
        )
        return event_registration

    def update(self, instance, validated_data):
        # Update the instance fields
        bank_data = validated_data.pop('bank_details', None)
        uploads_data = validated_data.pop('uploads', None)
        event_data = validated_data.pop('event_details', None)

        # Update fields directly on the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update related instances if provided
        if bank_data:
            for key, value in bank_data.items():
                setattr(instance.bank_details, key, value)
            instance.bank_details.save()

        if uploads_data:
            for key, value in uploads_data.items():
                setattr(instance.uploads, key, value)
            instance.uploads.save()

        if event_data:
            for key, value in event_data.items():
                setattr(instance.event_details, key, value)
            instance.event_details.save()

        return instance


class InternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = [
            'name', 'designation', 
            'email', 'mobile_number', 'organisation_name',
            'intern_method', 'internship_title', 'skills_list', 
            'internship_type', 'type_of_work', 'start_date', 
            'end_date', 'job_responsibilities', 'duration'
        ] 

class ApprenticeshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apprenticeship
        fields = [
            'name', 'designation', 
            'email', 'mobile_number', 'organisation_name',
            'apprenticeship_method', 'apprenticeship_title', 
            'skills_list', 'apprenticeship_type', 'type_of_work', 
            'start_date', 'end_date', 'job_responsibilities', 'duration'
        ]

