# urls.py
from django.urls import path
from .views import GigWorkFormView
from .views import CastingCallFormView, ProjectFormView,PostFeedView
from .views import EventRegistrationCreateView, InternshipCreateView, ApprenticeshipCreateView



urlpatterns = [
    path('gigwork/form/', GigWorkFormView.as_view(), name='gigwork_form'),
    path('castingcall/form/', CastingCallFormView.as_view(), name='castingcall_form'),
    path('project/form/', ProjectFormView.as_view(), name='project_form'),
    path('postfeeds/form/', PostFeedView.as_view(), name='postfeed'),
    path('event/form/', EventRegistrationCreateView.as_view(), name='event-registration'),
    path('internship/form/', InternshipCreateView.as_view(), name='internship-application'),
    path('apprenticeship/form/', ApprenticeshipCreateView.as_view(), name='apprenticeship-application'),

    
]