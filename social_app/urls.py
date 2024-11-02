from django.urls import path
from .views import (
    FollowRequestViewSet,
    BlockViewSet,
    ListFollowersView,
    ListFollowingView,
)

urlpatterns = [
    path('users/<int:user_id>/followers/', ListFollowersView.as_view(), name='list_followers'),
    path('users/<int:user_id>/following/', ListFollowingView.as_view(), name='list_following'),
    path('users/<int:user_id>/follow/send/', FollowRequestViewSet.as_view({'post': 'send_request'}), name='send_follow_request'),
    path('users/<int:user_id>/follow/accept/', FollowRequestViewSet.as_view({'post': 'accept_request'}), name='accept_follow_request'),
    path('users/<int:user_id>/follow/cancel/', FollowRequestViewSet.as_view({'post': 'cancel_request'}), name='cancel_follow_request'),
    path('users/<int:user_id>/unfollow/', FollowRequestViewSet.as_view({'post': 'unfollow'}), name='unfollow_user'),
    path('users/<int:user_id>/block/', BlockViewSet.as_view({'post': 'block_user'}), name='block_user'),
    path('users/<int:user_id>/unblock/', BlockViewSet.as_view({'delete': 'unblock_user'}), name='unblock_user'),
    path('users/follow-requests/', FollowRequestViewSet.as_view({'get': 'list_requests'}), name='list_follow_requests'),
]
