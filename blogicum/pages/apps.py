"""Application configuration."""
from django.apps import AppConfig


class PagesConfig(AppConfig):
    """Configure the pages application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'
