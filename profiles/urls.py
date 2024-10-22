from django.urls import path
from .views import IndustryListView, SkillListView ,UserProfileView
from .views import get_user_by_id

urlpatterns = [
    path('user_profile/', UserProfileView.as_view(), name='update_profile'),
    path('api/user/<str:user_id>/', get_user_by_id, name='get_user_by_id'),
    path('getindustry/', IndustryListView.as_view(), name='get-industry'),
    path('getskills/', SkillListView.as_view(), name='get-skills'),
]