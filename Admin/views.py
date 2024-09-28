from rest_framework import viewsets
from .serializer import UserSerializer,TeacherSerializer,CourseSerializer,DepartmentSerializer,VideoSerializer,ContactSerializer,ReviewSerializer,WeekSerializer,EnrollCourseSerializer
from accounts.models import User
from teacher.models import TeacherModel
from Enroll.models import EnrolledCourseModel
from course.models import CourseModel,VideoModel,ReviewModel, WeekModule
from department.models import DepartmentModel
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import PermissionDenied
from .models import ContactModel
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
# Create your views here.

class AdminCheckMixin:
    def check_admin(self, request):
        user_id = self.kwargs.get('user_id')  # Fetch the user ID from the URL
        if not user_id:
            raise PermissionDenied({"error": "User ID is required."})

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise PermissionDenied({"error": "User not found."})

        # Check if the user is an admin
        if not user.is_staff:
            raise PermissionDenied({"error": "You do not have permission to perform this action."})


class StudentApiView(AdminCheckMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        self.check_admin(self.request)  # Check admin status here
        return super().get_queryset()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=200)
        else:
            # Return the validation errors in the response for better debugging
            return Response(serializer.errors, status=400)


class TeasherApiView(AdminCheckMixin, viewsets.ModelViewSet):
    queryset = TeacherModel.objects.all()
    serializer_class = TeacherSerializer
    authentication_classes = [SessionAuthentication]
    parser_classes = [MultiPartParser, FormParser]  # Added JSONParser

    def get_queryset(self):
        self.check_admin(self.request)  # Check admin status here
        return super().get_queryset()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            self.perform_update(serializer)
            
            return Response(serializer.data, status=200)
        else:
            # Return the validation errors in the response for better debugging
            return Response(serializer.errors, status=400)


class CourseApiView(AdminCheckMixin, viewsets.ModelViewSet):
    queryset = CourseModel.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        self.check_admin(self.request)  # Check admin status here
        return super().get_queryset()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class VideoApiView(AdminCheckMixin, viewsets.ModelViewSet):
    queryset = VideoModel.objects.all()
    serializer_class = VideoSerializer
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        self.check_admin(self.request)  # Check admin status here
        return super().get_queryset()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class DepartmentApiView(AdminCheckMixin, viewsets.ModelViewSet):
    queryset = DepartmentModel.objects.all()
    serializer_class = DepartmentSerializer
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        self.check_admin(self.request)  # Check admin status here
        return super().get_queryset()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class ContactApiView(AdminCheckMixin, viewsets.ModelViewSet):
    queryset = ContactModel.objects.all()
    serializer_class = ContactSerializer
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        self.check_admin(self.request)  # Check admin status here
        return super().get_queryset()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class ReviewApiView(AdminCheckMixin, viewsets.ModelViewSet):
    queryset = ReviewModel.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        self.check_admin(self.request)  # Check admin status here
        return super().get_queryset()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        serializer = self.get_serializer(instance=self.get_object(), data=request.data, partial=True)
        if not serializer.is_valid():
            print(serializer.errors)  # Log validation errors for debugging
            return Response(serializer.errors, status=400)
        return super().partial_update(request, *args, **kwargs)


class WeekApiView(AdminCheckMixin, viewsets.ModelViewSet):
    queryset = WeekModule.objects.all()
    serializer_class = WeekSerializer
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        self.check_admin(self.request)  # Check admin status here
        return super().get_queryset()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class EnrollApiView(AdminCheckMixin, viewsets.ModelViewSet):
    queryset = EnrolledCourseModel.objects.all()
    serializer_class = EnrollCourseSerializer
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        self.check_admin(self.request)  # Check admin status here
        return super().get_queryset()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
