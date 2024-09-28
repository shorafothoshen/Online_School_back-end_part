from rest_framework import serializers
from accounts.models import User
from course.models import CourseModel,VideoModel,ReviewModel, WeekModule
from teacher.models import TeacherModel
from department.models import DepartmentModel
from .models import ContactModel
from Enroll.models import EnrolledCourseModel

GENDER_TYPE = (
    ("Male", "Male"),
    ("Female", "Female"),
)

RATING = (
    (1, "⭐"),
    (2, "⭐⭐"),
    (3, "⭐⭐⭐"),
    (4, "⭐⭐⭐⭐"),
    (5, "⭐⭐⭐⭐⭐"),
)

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True, required=False)
    confirm_password = serializers.CharField(style={"input_type": "password"}, write_only=True, required=False)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "gender", "birthday", "image", "is_teacher", "is_staff", 'password', 'confirm_password']

    # Ensure passwords match if both are provided
    def validate(self, data):
        request = self.context.get('request')
        if request.method == "POST":  # For create
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            
            if not password or not confirm_password:
                raise serializers.ValidationError({'error': "Password and Confirm Password are required."})
            
            if password != confirm_password:
                raise serializers.ValidationError({'error': "Passwords do not match."})
        return data

    def create(self, validated_data):
        # Remove confirm_password from validated_data
        validated_data.pop('confirm_password', None)
        password = validated_data.pop('password', None)  
        # Create the user
        account = super().create(validated_data)
        if password:
            account.set_password(password)
        
        account.is_active = True
        account.save()
        
        return account

    def update(self, instance, validated_data):
        request = self.context.get('request')
        
        # If it's an admin, ignore the password field during updates
        if request.user.is_staff and 'password' in validated_data:
            validated_data.pop('password')

        instance = super().update(instance, validated_data)
        return instance

    
class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    department=serializers.StringRelatedField(many=False)
    class Meta:
        model = TeacherModel
        fields = ["id","user", "department","bio", "Country", "City"]

    def create(self, validated_data):
        # Extract user data and remove it from validated_data
        user_data = validated_data.pop('user')
        print(user_data)
        # Create the user and set `is_teacher=True`
        user_serializer = UserSerializer(data=user_data, context=self.context)
        if user_serializer.is_valid(raise_exception=True):
            
            user = user_serializer.save(is_teacher=True)  # Automatically sets is_teacher
            print(user)
        # Create the teacher model with the created user
        teacher = TeacherModel.objects.create(user=user, **validated_data)
        print(teacher)
        return teacher

    def update(self, instance, validated_data):
        # Extract user data for update if provided
        user_data = validated_data.pop('user', None)
        if user_data:
            # Perform partial update on user fields
            user_serializer = UserSerializer(instance=instance.user, data=user_data, partial=True, context=self.context)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()

        # Update other teacher fields
        return super().update(instance, validated_data)


class CourseSerializer(serializers.ModelSerializer):
    instructor = TeacherSerializer()
    department=serializers.StringRelatedField(many=False)
    class Meta:
        model=CourseModel
        fields="__all__"

class WeekSerializer(serializers.ModelSerializer):
    course=serializers.StringRelatedField(many=False)
    class Meta:
        model=WeekModule
        fields='__all__'


class VideoSerializer(serializers.ModelSerializer):
    course=serializers.StringRelatedField(many=False)
    week=WeekSerializer()
    class Meta:
        model=VideoModel
        fields="__all__"

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=DepartmentModel
        fields="__all__"


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model=ContactModel
        fields='__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    rating = serializers.ChoiceField(choices=RATING, write_only=True)
    rating_display = serializers.SerializerMethodField() 
    course=serializers.StringRelatedField(many=False)

    class Meta:
        model = ReviewModel
        fields = ["id",'course','user', 'rating', 'rating_display', 'body', 'created_on']
        read_only_fields = ['rating_display', 'user', 'created_on'] 

    def get_rating_display(self, obj):
        return dict(RATING).get(obj.rating, "No rating")

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class EnrollCourseSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    course=CourseSerializer()
    class Meta:
        model=EnrolledCourseModel
        fields='__all__'
        