
from rest_framework.authtoken import views
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'reviews', views.ReviewViewSet, basename='review'),
router.register(r'show-review', views.ShowReview, basename='showreview')
urlpatterns = [
    path("",views.CourseAPIView.as_view(), name="course"),
    path("<int:course_id>/videos/", views.CourseVideosApiView.as_view(), name="course-videos"), 
    path('<int:pk>/', views.CourseRetrieveAPIView.as_view(), name='course-detail'),
    path("video/<int:pk>/",views.VideoApiView.as_view(), name="videos"),
    path('', include(router.urls)),
]
