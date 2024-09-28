from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/account/",include("accounts.urls")),
    path("api/course/",include("course.urls")),
    path("api/teachers/",include("teacher.urls")),
    path("payment/",include("Enroll.urls")),
    path("",include("Admin.urls")),
    path("auth/",include("rest_framework.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)