from rest_framework import serializers

class DashboardStatsSerializer(serializers.Serializer):
    """
    Serializer wrapping dashboard statistics analytics structures.
    """
    total = serializers.IntegerField()
    resolved = serializers.IntegerField()
    pending = serializers.IntegerField()
    escalated = serializers.IntegerField()
    failures = serializers.IntegerField()
    departments = serializers.ListField()
    states = serializers.ListField()
    cities = serializers.ListField()
    mapPins = serializers.ListField()
    user = serializers.DictField(required=False, allow_null=True)
