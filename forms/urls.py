# urls.py
from django.urls import path
from .views import GigWorkFormView
from .views import CastingCallFormView, ProjectFormView,PostFeedView
from .views import EventRegistrationCreateView, InternshipCreateView, ApprenticeshipCreateView



urlpatterns = [
    path('gigwork/form/', GigWorkFormView.as_view(), name='gigwork_form'),  # POST
    path('gigwork/form/<int:pk>/', GigWorkFormView.as_view(), name='gigwork_form_detail'),  # GET, PUT, DELETE
    path('castingcall/form/', CastingCallFormView.as_view(), name='castingcall_form'),
    path('castingcall/form/<int:pk>/', CastingCallFormView.as_view(), name='castingcall_form_detail'),  
    path('project/form/', ProjectFormView.as_view(), name='project_form'),
    path('project/form/<int:pk>/', ProjectFormView.as_view(), name='project_form_detail'),  
    path('postfeeds/form/', PostFeedView.as_view(), name='postfeed'),
    path('postfeeds/form/<int:pk>/', PostFeedView.as_view(), name='postfeed_detail'), 
    path('event/form/', EventRegistrationCreateView.as_view(), name='event-registration'),
    path('event/form/<int:user_id>/', EventRegistrationCreateView.as_view(), name='event_registration_detail'),  
    path('internship/form/', InternshipCreateView.as_view(), name='internship-application'),
    path('internship/form/<int:user_id>/', InternshipCreateView.as_view(), name='internship_detail'),
    path('apprenticeship/form/', ApprenticeshipCreateView.as_view(), name='apprenticeship-application'),
    path('apprenticeship/form/<int:user_id>/', ApprenticeshipCreateView.as_view(), name='apprenticeship_detail'),  
   
]
