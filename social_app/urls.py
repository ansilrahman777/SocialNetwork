from django.urls import path
from .views import (
    BlockReasonListView,
    FollowRequestViewSet,
    BlockViewSet,
    ListFollowersView,
    ListFollowingView,
    ReportReasonListView,
    ReportViewSet,
)

urlpatterns = [
    path('profile/<int:user_id>/followers/', ListFollowersView.as_view(), name='list_followers'),
    path('profile/<int:user_id>/following/', ListFollowingView.as_view(), name='list_following'),
    path('profile/<int:user_id>/follow/send/', FollowRequestViewSet.as_view({'post': 'send_request'}), name='send_follow_request'),
    path('profile/<int:user_id>/follow/accept/', FollowRequestViewSet.as_view({'post': 'accept_request'}), name='accept_follow_request'),
    path('profile/<int:user_id>/follow/cancel/', FollowRequestViewSet.as_view({'post': 'cancel_request'}), name='cancel_follow_request'),
    path('profile/<int:user_id>/follow/reject/', FollowRequestViewSet.as_view({'post': 'reject_request'}), name='reject_follow_request'),
    path('profile/<int:user_id>/unfollow/', FollowRequestViewSet.as_view({'post': 'unfollow'}), name='unfollow_user'),
    path('profile/follow-requests/', FollowRequestViewSet.as_view({'get': 'list_requests'}), name='list_follow_requests'),
    path('profile/<int:user_id>/block/', BlockViewSet.as_view({'post': 'block_user'}), name='block_user'),
    path('profile/<int:user_id>/unblock/', BlockViewSet.as_view({'delete': 'unblock_user'}), name='unblock_user'),
    path('profile/<int:user_id>/report/', ReportViewSet.as_view({'post': 'report_user'}), name='report_user'),
    path('profile/block-reasons/', BlockReasonListView.as_view(), name='block_reasons'),
    path('profile/report-reasons/', ReportReasonListView.as_view(), name='report_reasons'),
]
