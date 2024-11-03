from rest_framework import serializers
from .models import FollowRequest, Follow, Block, Report
from userprofile_app.models import Profile

class FollowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowRequest
        fields = '__all__'

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

class BlockSerializer(serializers.ModelSerializer):
    common_reason = serializers.ChoiceField(choices=Block.COMMON_BLOCK_REASONS, required=False)
    reason_details = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Block
        fields = ['blocked', 'common_reason', 'reason_details', 'blocked_at']
        read_only_fields = ['blocked_at']

    def validate_common_reason(self, value):
        if value and value not in dict(Block.COMMON_BLOCK_REASONS).keys():
            raise serializers.ValidationError("Invalid block reason.")
        return value

class ReportSerializer(serializers.ModelSerializer):
    common_reason = serializers.ChoiceField(choices=Report.COMMON_REPORT_REASONS, required=False)
    details = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Report
        fields = ['reported', 'common_reason', 'details', 'reported_at']
        read_only_fields = ['reported_at']

    def validate_common_reason(self, value):
        if value and value not in dict(Report.COMMON_REPORT_REASONS).keys():
            raise serializers.ValidationError("Invalid report reason.")
        return value

class ReasonSerializer(serializers.Serializer):
    code = serializers.CharField()
    label = serializers.CharField()
