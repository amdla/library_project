# library_project/urls.py

from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library_app.urls')),
    path('', RedirectView.as_view(url='/books/', permanent=True)),  # Przekierowanie z głównej strony na listę książek
]
