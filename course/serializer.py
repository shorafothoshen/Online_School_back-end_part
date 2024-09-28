from rest_framework import serializers
from .models import CourseModel, VideoModel, WeekModule,ReviewModel
from teacher.serializer import TeacherSerializer
from accounts.serializer import UserProfileSerializer

RATING = (
    (1, "⭐"),
    (2, "⭐⭐"),
    (3, "⭐⭐⭐"),
    (4, "⭐⭐⭐⭐"),
    (5, "⭐⭐⭐⭐⭐"),
)

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoModel
        fields = ["id","course","week", "title", "description", "video_file"]

class WeekSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)
    class Meta:
        model = WeekModule
        fields = ["id","course", "name", "videos"]

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewModel
        fields = '__all__'

class ReviewSerializer2(serializers.ModelSerializer):
    user=UserProfileSerializer(many=False, read_only=True)
    rating = serializers.ChoiceField(choices=RATING, write_only=True)
    rating_display = serializers.SerializerMethodField() 
    course=serializers.StringRelatedField(many=False)

    class Meta:
        model = ReviewModel
        fields = ['course','user', 'rating', 'rating_display', 'body', 'created_on']
        read_only_fields = ['rating_display', 'user', 'created_on'] 

    def get_rating_display(self, obj):
        return dict(RATING).get(obj.rating, "No rating")

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class CourseSerializer(serializers.ModelSerializer):
    instructor = TeacherSerializer(many=False, read_only=True)
    department = serializers.StringRelatedField(many=False)
    reviews = ReviewSerializer2(many=True, read_only=True)

    class Meta:
        model = CourseModel
        fields = ["id", "title", "instructor", "department", "amount", "description", "created_at", "image", "reviews"]