from django.urls import path
from .views import ShortenURLView, RedirectURLView, URLAnalyticsView

urlpatterns = [
    path('url/shorten', ShortenURLView.as_view(),
         name='shorten_url'),         # For shortening URLs
    path('r/<str:short_id>', RedirectURLView.as_view(),
         name='redirect_url'),   # For redirecting short URLs
    path('analytics/<str:short_id>', URLAnalyticsView.as_view(),
         name='url_analytics'),  # For URL analytics
]
