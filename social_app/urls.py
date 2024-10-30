from django.urls import path
from .views import FollowViewSet, FollowRequestViewSet, BlockViewSet

urlpatterns = [
    path('follow/<int:user_id>/', FollowViewSet.as_view({'post': 'follow'})),
    path('unfollow/<int:user_id>/', FollowViewSet.as_view({'delete': 'unfollow'})),
    path('following/', FollowViewSet.as_view({'get': 'list_following'})),
    path('followers/', FollowViewSet.as_view({'get': 'list_followers'})),
    path('follow-request/send/<int:user_id>/', FollowRequestViewSet.as_view({'post': 'send_request'})),
    path('follow-request/accept/<int:request_id>/', FollowRequestViewSet.as_view({'post': 'accept_request'})),
    path('follow-request/cancel/<int:request_id>/', FollowRequestViewSet.as_view({'post': 'cancel_request'})),
    path('block/<int:user_id>/', BlockViewSet.as_view({'post': 'block_user'})),
    path('unblock/<int:user_id>/', BlockViewSet.as_view({'delete': 'unblock_user'})),
]
