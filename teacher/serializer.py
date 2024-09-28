from rest_framework import serializers
from .models import TeacherModel
from accounts.models import User
from course.models import CourseModel,WeekModule
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'gender', 'birthday', 'is_teacher', 'image']

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department=serializers.StringRelatedField(many=False)
    class Meta:
        model = TeacherModel
        fields = ['id', 'user', 'department','bio', 'Country', 'City']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModel
        fields = ["id", "title", "instructor", "department", "amount", "description", "created_at", "image"]  # Include the fields you need
        read_only_fields = ['instructor', 'department']
class WeekModuleSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(write_only=True)  # Expect course_id from the front-end

    class Meta:
        model = WeekModule
        fields = ['id', 'name', 'course_id']

    def validate(self, data):
        # Get the request object from the context
        request = self.context.get('request')

        # Fetch the user_id from the URL
        user_id = self.context.get('view').kwargs.get('user_id')

        # Fetch the teacher using the user_id from the URL
        teacher = get_object_or_404(TeacherModel, user_id=user_id)

        # Ensure the teacher is the instructor for the course
        course_id = data.get('course_id')
        course = get_object_or_404(CourseModel, id=course_id, instructor=teacher)

        # Attach the course to the week instance if validation passes
        data['course'] = course
        return data