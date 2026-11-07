"""Application configuration."""
from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Configure the blog application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = 'Блог'
