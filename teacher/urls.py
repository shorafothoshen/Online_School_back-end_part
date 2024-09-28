from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .import views

router = DefaultRouter()
router.register(r'courses', views.TeacherCourseApiView, basename='teacher-courses')
router.register(r'videos', views.TeacherVideoApiView, basename='teacher-videos')

urlpatterns = [
    path("", views.TeacherListApiView.as_view(), name="teachers"),
    path("<int:pk>/", views.TeacherRetrieveApiView.as_view(), name="teacher-detail"),
    path("user/<int:user_id>/", views.TeacherRetrieveApi.as_view(), name="teacher_detail"),
    path('<int:user_id>/courses/<int:course_id>/weeks/', views.WeekModuleView.as_view(), name='course-weeks'),
    path('<int:user_id>/courses/<int:course_id>/videos/', views.TeacherCourseVideosView.as_view(), name='teacher-course-videos'),
    path("<int:user_id>/", include(router.urls)),
]
