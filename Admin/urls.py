from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from . import views

router=DefaultRouter()

router.register("User",views.StudentApiView,basename="adminStudent")
router.register("teacher",views.TeasherApiView,basename="adminTeacher")
router.register("course",views.CourseApiView,basename="adminCourse")
router.register("CourseVideo",views.VideoApiView,basename="adminCourseVideo")
router.register("Department",views.DepartmentApiView,basename="adminDepartment")
router.register("contact",views.ContactApiView,basename="contact")
router.register("reviews",views.ReviewApiView,basename="reviews")
router.register("weeks",views.WeekApiView,basename="weeks")
router.register("enrolled",views.EnrollApiView,basename="enrolled")

urlpatterns = [
    path("api/admin/<int:user_id>/",include(router.urls)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)