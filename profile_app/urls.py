from django.urls import path
from .views import IndustryListView, SkillListView ,UserProfileView
from .views import  AadharVerificationView, PassportVerificationView, DriverLicenseVerificationView
from .views import get_user_by_id

urlpatterns = [
    path('profile_create/', UserProfileView.as_view(), name='profile-create'),
    path('api/user/<str:user_id>/', get_user_by_id, name='get_user_by_id'),
    path('getindustry/', IndustryListView.as_view(), name='get-industry'),
    path('getskills/', SkillListView.as_view(), name='get-skills'),
    path('docverifyaadhar/', AadharVerificationView.as_view(), name='aadhar-verification'),
    path('docverifypassport/', PassportVerificationView.as_view(), name='passport-verification'),
    path('docverifydl/', DriverLicenseVerificationView.as_view(), name='dl-verification'),
]