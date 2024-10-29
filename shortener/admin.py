from django.contrib import admin
from .models import URL

class URLAdmin(admin.ModelAdmin):
    list_display = ('original_url', 'short_id', 'custom_slug', 'created_at', 'expires_at', 'access_count')
    search_fields = ('original_url', 'short_id', 'custom_slug')
    list_filter = ('created_at', 'expires_at')

    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True  # Display a boolean icon in the admin interface
    is_expired.short_description = 'Expired'

admin.site.register(URL, URLAdmin)
