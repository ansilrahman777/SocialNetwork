from django.urls import path
from .views import (
    DocumentUploadView, DocumentVerificationViewSet, ProfileViewSet, RoleListView, RoleSelectionView, IndustryListView, IndustrySelectionView,
    PrimaryIndustrySelectionView, SkillListView, SkillSelectionView,
    PrimarySkillSelectionView,
    ExperienceViewSet, EducationViewSet, UnionAssociationViewSet
)

urlpatterns = [
    # Role endpoints
    path('profile/roles/', RoleListView.as_view({'get': 'list'}), name='role-list'),
    path('profile/join-as/', RoleSelectionView.as_view({'post': 'create'}), name='join-as'),
    path('profile/join-as/<int:user_id>/', RoleSelectionView.as_view({'patch': 'update'}), name='role-update'),

    # Industry endpoints
    path('profile/get-industries/', IndustryListView.as_view({'get': 'list'}), name='industry-list'),
    path('profile/select-industries/', IndustrySelectionView.as_view({'post': 'create'}), name='industry-select'),
    path('profile/select-industries/<int:user_id>/', IndustrySelectionView.as_view({'patch': 'update', 'delete': 'destroy'}), name='industry-edit-delete'),
    path('profile/primary-industry/', PrimaryIndustrySelectionView.as_view({'post': 'create'}), name='primary-industry-select'),
    path('profile/primary-industry/<int:user_id>/', PrimaryIndustrySelectionView.as_view({'patch': 'update', 'delete': 'destroy'}), name='primary-industry-edit-delete'),
      
    # Skill endpoints
    path('profile/get-skills/', SkillListView.as_view({'get': 'list'}), name='skill-list'),
    path('profile/select-skills/', SkillSelectionView.as_view({'post': 'create'}), name='skill-select'),
    path('profile/select-skills/<int:user_id>/', SkillSelectionView.as_view({'patch': 'update', 'delete': 'destroy'}), name='skill-edit-delete'),
    path('profile/primary-skill/', PrimarySkillSelectionView.as_view({'post': 'create'}), name='primary-skill-select'),
    path('profile/primary-skill/<int:user_id>/', PrimarySkillSelectionView.as_view({'patch': 'update', 'delete': 'destroy'}), name='primary-skill-edit-delete'),

    # Profile create, edit and detail
    path('profile/create/', ProfileViewSet.as_view({'post': 'create'}), name='profile-create'),
    path('profile/<int:user_id>/', ProfileViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='profile-detail-edit'),
    path('profile/<int:user_id>/profile-completion/', ProfileViewSet.as_view({'get': 'profile_completion'}), name='profile-completion-status'),

    # Experience endpoints
    path('profile/experience/', ExperienceViewSet.as_view({'post': 'create'}), name='experience-add'),
    path('profile/<int:user_id>/experience/', ExperienceViewSet.as_view({'get': 'list'}), name='user-experience'),
    path('profile/experience/<int:pk>/', ExperienceViewSet.as_view({'patch': 'update', 'delete': 'destroy'}), name='experience-detail'),

    # Education endpoints
    path('profile/education/', EducationViewSet.as_view({'post': 'create'}), name='education-add'),
    path('profile/<int:user_id>/education/', EducationViewSet.as_view({'get': 'list'}), name='user-education'),
    path('profile/education/<int:pk>/', EducationViewSet.as_view({'patch': 'update', 'delete': 'destroy'}), name='education-detail'),
    
    # Document verification 
    path('profile/docverifyaadhar/', DocumentVerificationViewSet.as_view({'post': 'verify_aadhar'}), name='doc-verify-aadhar'),
    path('profile/docverifypassport/', DocumentVerificationViewSet.as_view({'post': 'verify_passport'}), name='doc-verify-passport'),
    path('profile/docverifydl/', DocumentVerificationViewSet.as_view({'post': 'verify_dl'}), name='doc-verify-dl'),
    path('profile/docupload/', DocumentUploadView.as_view({'post': 'create'}), name='doc-upload'),
    
    # UnionAssociation endpoints
    path('profile/union-association/', UnionAssociationViewSet.as_view({'post': 'create'}), name='union-association-add'),
    path('profile/<int:user_id>/union-association/', UnionAssociationViewSet.as_view({'get': 'list'}), name='user-union-association'),
    path('profile/union-association/<int:pk>/', UnionAssociationViewSet.as_view({'patch': 'update', 'delete': 'destroy'}), name='union-association-detail'),

]
