from django.db import models
from django.utils import timezone
from datetime import timedelta
import string
import random


class URL(models.Model):
    original_url = models.URLField(unique=True)
    short_id = models.CharField(
        max_length=8, unique=True, blank=True, null=True)
    custom_slug = models.CharField(
        max_length=30, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    access_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.custom_slug and not self.short_id:
            self.short_id = None
        elif not self.short_id and not self.custom_slug:
            self.short_id = self.generate_short_id()
        super().save(*args, **kwargs)

    def generate_short_id(self):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(8))

    def is_expired(self):
        return self.expires_at and timezone.now() > self.expires_at
