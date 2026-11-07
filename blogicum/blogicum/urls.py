"""Main routes and custom error handlers."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.urls import include, path, reverse_lazy
from django.views.generic import CreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/registration/', CreateView.as_view(
        form_class=UserCreationForm,
        template_name='registration/registration_form.html',
        success_url=reverse_lazy('login'),
    ), name='registration'),
    path('auth/', include('django.contrib.auth.urls')),
    path('pages/', include('pages.urls')),
    path('', include('blog.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'
