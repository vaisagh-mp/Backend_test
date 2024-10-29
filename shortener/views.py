from django.utils import timezone
from django.db import models
from django.db.models import Q
from rest_framework import status
from django.shortcuts import redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from .models import URL
from .serializers import URLSerializer
from django.http import JsonResponse


class ShortenURLView(APIView):
    def post(self, request):
        serializer = URLSerializer(data=request.data)
        if serializer.is_valid():
            custom_slug = serializer.validated_data.get('custom_slug')
            short_id = serializer.validated_data.get('short_id')

            # Check for custom slug uniqueness
            if custom_slug and URL.objects.filter(custom_slug=custom_slug).exists():
                return Response({"error": "Custom slug already in use."}, status=status.HTTP_400_BAD_REQUEST)

            # Create the URL object
            url_obj = serializer.save()

            # Generate the short URL using provided short_id or custom_slug
            short_url = f"http://localhost:8000/r/{custom_slug or url_obj.short_id}"
            return Response({'short_url': short_url}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(ratelimit(key='ip', rate='1/minute', method='GET', block=False), name='dispatch')
class RedirectURLView(APIView):
    def get(self, request, short_id):
        # Check if the request was rate limited
        if getattr(request, 'limited', False):
            return JsonResponse({"error": "Access limit exceeded. Please try again later."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        url_obj = URL.objects.filter(
            models.Q(short_id=short_id) | models.Q(custom_slug=short_id)).first()

        if not url_obj:
            return JsonResponse({"error": "Short URL not found."}, status=status.HTTP_404_NOT_FOUND)

        if url_obj.is_expired():
            return JsonResponse({"error": "Short URL has expired."}, status=status.HTTP_410_GONE)

        # Track access count
        url_obj.access_count += 1
        url_obj.save(update_fields=['access_count'])

        return redirect(url_obj.original_url)


class URLAnalyticsView(APIView):
    def get(self, request, short_id):
        url_obj = get_object_or_404(URL, models.Q(
            short_id=short_id) | models.Q(custom_slug=short_id))
        return Response({
            "original_url": url_obj.original_url,
            "access_count": url_obj.access_count,
            "created_at": url_obj.created_at,
            "expires_at": url_obj.expires_at,
            "is_expired": url_obj.is_expired()
        })
