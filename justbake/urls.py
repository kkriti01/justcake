from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from cakes.views import CakeView, FetchCakes, ExportCakes

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', CakeView.as_view(), name='home'),
    url(r'^fetch-cakes$', FetchCakes.as_view(), name='fetch_cakes'),
    url(r'^export-cakes$', ExportCakes.as_view(), name='export_cakes'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
