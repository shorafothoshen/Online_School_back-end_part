from django.shortcuts import render
from .serializer import TeacherSerializer,WeekModuleSerializer
from .models import TeacherModel
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from course.models import CourseModel, VideoModel, WeekModule
from course.serializer import VideoSerializer, CourseSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

class TeacherListApiView(ListAPIView):
    queryset = TeacherModel.objects.all()
    serializer_class = TeacherSerializer

class TeacherRetrieveApiView(RetrieveAPIView):
    queryset = TeacherModel.objects.all()
    serializer_class = TeacherSerializer


class TeacherRetrieveApi(RetrieveAPIView):
    queryset = TeacherModel.objects.all()
    serializer_class = TeacherSerializer
    lookup_field = 'user_id'

    def get_queryset(self):
        user_id = self.kwargs['user_id'] 
        return TeacherModel.objects.filter(user_id=user_id)

class WeekModuleView(generics.ListCreateAPIView):
    serializer_class = WeekModuleSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        teacher = get_object_or_404(TeacherModel, user_id=user_id)
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(CourseModel, id=course_id, instructor=teacher)
        return WeekModule.objects.filter(course=course)

    def perform_create(self, serializer):
        user_id = self.kwargs.get('user_id')
        teacher = get_object_or_404(TeacherModel, user_id=user_id)
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(CourseModel, id=course_id, instructor=teacher)
        serializer.save(course=course)

class TeacherCourseApiView(ModelViewSet):
    serializer_class = CourseSerializer
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        teacher = get_object_or_404(TeacherModel, user__id=user_id)
        return CourseModel.objects.filter(instructor=teacher)

    def perform_create(self, serializer):
        user_id = self.kwargs.get('user_id')
        teacher = get_object_or_404(TeacherModel, user__id=user_id)
        serializer.save(instructor=teacher, department=teacher.department)


class TeacherVideoApiView(ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = VideoSerializer
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        course_id = self.request.query_params.get("course_id")
        user_id = self.request.data.get("user_id")

        teacher_user = get_object_or_404(get_user_model(), id=user_id)

        if not hasattr(teacher_user, 'teacher'):
            raise PermissionDenied("You do not have permission to access this resource.")
        course = get_object_or_404(CourseModel, id=course_id, instructor=teacher_user.teacher)
        return VideoModel.objects.filter(week__course=course)

    def perform_create(self, serializer):
        course_id = self.request.data.get("course_id")
        week_id = self.request.data.get("week")
        title = self.request.data.get("title")
        description = self.request.data.get("description")
        video_file = self.request.FILES.get("video_file")
        user_id = self.request.data.get("user_id") 

        teacher_user = get_object_or_404(get_user_model(), id=user_id)

        if not hasattr(teacher_user, 'teacher'):
            raise PermissionDenied("You do not have permission to perform this action.")
        
        course = get_object_or_404(CourseModel, id=course_id, instructor=teacher_user.teacher)
        week = get_object_or_404(WeekModule, id=week_id, course=course)
        video = VideoModel.objects.create(
            course=course,
            week=week,
            title=title,
            description=description,
            video_file=video_file
        )

        return Response({"detail": "Video uploaded successfully", "video_id": video.id}, status=201)
    

class TeacherCourseVideosView(generics.ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        teacher = get_object_or_404(TeacherModel, user_id=user_id)
        course_id = self.kwargs.get('course_id') or self.request.query_params.get('course_id')
        course = get_object_or_404(CourseModel, id=course_id, instructor=teacher)
        return VideoModel.objects.filter(course=course)
