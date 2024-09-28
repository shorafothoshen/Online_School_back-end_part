from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView,RetrieveAPIView
from .models import CourseModel,WeekModule,VideoModel,ReviewModel
from .serializer import CourseSerializer,WeekSerializer,VideoSerializer,ReviewSerializer,ReviewSerializer2
from rest_framework.views import APIView
from rest_framework import viewsets,filters
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import VideoModel
from django.shortcuts import get_object_or_404
# Create your views here.

class CourseAPIView(ListCreateAPIView):
    queryset=CourseModel.objects.all()
    serializer_class=CourseSerializer
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['title', 'amount', 'created_at']  # Fields to allow ordering by

class CourseRetrieveAPIView(RetrieveAPIView):
    queryset=CourseModel.objects.all()
    serializer_class=CourseSerializer


class CourseVideosApiView(ListAPIView):
    serializer_class = WeekSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return WeekModule.objects.filter(course_id=course_id)

    def get(self, request, *args, **kwargs):
        weeks = self.get_queryset()
        serializer = self.get_serializer(weeks, many=True)
        return Response(serializer.data)

class VideoApiView(RetrieveAPIView):
    queryset=VideoModel.objects.all()
    serializer_class=VideoSerializer
    
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = ReviewModel.objects.all()
    serializer_class = ReviewSerializer
    ordering = ['created_at'] 

class ShowReview(viewsets.ModelViewSet):
    queryset=ReviewModel.objects.all()
    serializer_class=ReviewSerializer2
