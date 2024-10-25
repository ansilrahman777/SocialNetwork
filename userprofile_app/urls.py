from django.urls import path
from .views import (
    RoleListView, RoleSelectionView, IndustryListView, IndustrySelectionView,
    PrimaryIndustrySelectionView, SkillListView, SkillSelectionView,
    PrimarySkillSelectionView, ProfileCreateView, ProfileDetailView,
    ExperienceViewSet, EducationViewSet
)

urlpatterns = [
    # Role endpoints
    path('profile/roles/', RoleListView.as_view({'get': 'list'}), name='role-list'),
    path('profile/join-as/', RoleSelectionView.as_view({'post': 'create'}), name='join-as'),
    path('profile/join-as/<int:user_id>/', RoleSelectionView.as_view({'patch': 'update'}), name='role-update'),

    # Industry endpoints
    path('profile/get-industries/', IndustryListView.as_view({'get': 'list'}), name='industry-list'),
    path('profile/select-industries/', IndustrySelectionView.as_view({'post': 'create'}), name='industry-select'),
    path('profile/primary-industry/', PrimaryIndustrySelectionView.as_view({'post': 'create'}), name='primary-industry-select'),

    # Skill endpoints
    path('profile/get-skills/', SkillListView.as_view({'get': 'list'}), name='skill-list'),
    path('profile/select-skills/', SkillSelectionView.as_view({'post': 'create'}), name='skill-select'),
    path('profile/primary-skill/', PrimarySkillSelectionView.as_view({'post': 'create'}), name='primary-skill-select'),

    # Profile creation and detail
    path('profile/create/', ProfileCreateView.as_view({'post': 'create'}), name='profile-create'),
    path('profile/<int:user_id>/', ProfileDetailView.as_view({'get': 'retrieve'}), name='profile-detail'),

    # Experience endpoints
    path('profile/experience/', ExperienceViewSet.as_view({'post': 'create'}), name='experience-add'),
    path('profile/<int:user_id>/experience/', ExperienceViewSet.as_view({'get': 'list'}), name='user-experience'),
    path('profile/experience/<int:pk>/', ExperienceViewSet.as_view({'patch': 'update', 'delete': 'destroy'}), name='experience-detail'),

    # Education endpoints
    path('profile/education/', EducationViewSet.as_view({'post': 'create'}), name='education-add'),
    path('profile/<int:user_id>/education/', EducationViewSet.as_view({'get': 'list'}), name='user-education'),
    path('profile/education/<int:pk>/', EducationViewSet.as_view({'patch': 'update', 'delete': 'destroy'}), name='education-detail'),
]
