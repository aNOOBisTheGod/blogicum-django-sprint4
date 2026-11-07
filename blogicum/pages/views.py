"""Custom error responses and static pages."""
from django.shortcuts import render
from django.views.generic import TemplateView


class AboutView(TemplateView):
    """Describe the community."""

    template_name = 'pages/about.html'


class RulesView(TemplateView):
    """Show community rules."""

    template_name = 'pages/rules.html'


def csrf_failure(request, reason=''):
    """Report invalid CSRF verification."""
    return render(request, 'pages/403csrf.html', status=403)


def page_not_found(request, exception):
    """Report missing resources."""
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    """Render a generic internal error page."""
    return render(request, 'pages/500.html', status=500)
