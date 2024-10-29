from rest_framework import serializers
from .models import URL
from datetime import timedelta
from django.utils import timezone


class URLSerializer(serializers.ModelSerializer):
    custom_slug = serializers.CharField(required=False)
    expires_in_days = serializers.IntegerField(write_only=True, required=False)
    short_id = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = URL
        fields = ['original_url', 'short_id', 'custom_slug', 'expires_in_days']

    def create(self, validated_data):
        expires_in_days = validated_data.pop('expires_in_days', None)
        short_id = validated_data.get('short_id')

        # Ensure short_id is unique if provided
        if short_id and URL.objects.filter(short_id=short_id).exists():
            raise serializers.ValidationError(
                {"short_id": "Short ID already in use."})

        # Create the URL object
        url_obj = URL.objects.create(**validated_data)

        # Set expiration date if provided
        if expires_in_days:
            url_obj.expires_at = timezone.now() + timedelta(days=expires_in_days)
            url_obj.save()

        return url_obj
