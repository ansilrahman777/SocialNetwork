# urls.py
from django.urls import path
from .views import (
    IndustryListView, SkillListView, RoleListView, RoleSelectionView,
    PrimaryIndustrySelectionView, PrimarySkillSelectionView,
    ExperienceViewSet, EducationViewSet, ProfileCreateView, 
)

urlpatterns = [
    path('profile/roles/', RoleListView.as_view({'get': 'list'}), name='role-list'),
    path('api/getindustry/', IndustryListView.as_view({'get': 'list'}), name='getindustry'),
    path('api/getskills/', SkillListView.as_view({'get': 'list'}), name='getskills'),
    path('profile/join-as/', RoleSelectionView.as_view({'post': 'create'}), name='join-as'),
    path('profile/choose_primary_industry/', PrimaryIndustrySelectionView.as_view({'post': 'create'}), name='choose_primary_industry'),
    path('profile/choose_primary_skills/', PrimarySkillSelectionView.as_view({'post': 'create'}), name='choose_primary_skills'),
    path('profile/experience/', ExperienceViewSet.as_view({'get': 'list', 'post': 'create'}), name='experience'),
    path('profile/education/', EducationViewSet.as_view({'get': 'list', 'post': 'create'}), name='education'),
    path('profile/create/', ProfileCreateView.as_view({'post': 'create'}), name='profile_create'),
    
]
