from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from game_check.game_review.views import page_does_not_exist

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('game_check.game_review.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)


handler404 = page_does_not_exist
