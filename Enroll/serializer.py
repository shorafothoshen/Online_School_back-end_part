from rest_framework import serializers
from django.shortcuts import get_object_or_404
from sslcommerz_lib import SSLCOMMERZ
from .models import CourseModel, EnrolledCourseModel
from accounts.models import User
import uuid
from course.serializer import CourseSerializer


class EnrolledCourseSerializer(serializers.ModelSerializer):
    course=CourseSerializer(many=False)
    class Meta:
        model = EnrolledCourseModel
        fields = ['user', 'course', 'enroll_date']

class EnrollCoursePaymentSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    course_id = serializers.IntegerField()

    def validate(self, data):
        try:
            user = User.objects.get(id=data['user_id'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        try:
            course = CourseModel.objects.get(id=data['course_id'])
        except CourseModel.DoesNotExist:
            raise serializers.ValidationError("Course does not exist")

        data['user'] = user
        data['course'] = course
        return data

    def create(self, validated_data):
        user = validated_data['user']
        course = validated_data['course']
        transaction_id = f'TXN-{uuid.uuid4().hex[:6].upper()}'
        # SSLCommerz Payment Gateway Configuration
        settings = {
            'store_id': 'carma66a892bde1cb7',
            'store_pass': 'carma66a892bde1cb7@ssl',
            'issandbox': True
        }
        sslcz = SSLCOMMERZ(settings)

        post_body = {
            'total_amount': course.amount,
            'currency': "BDT",
            'tran_id': transaction_id,
            'success_url': f'https://online-school-project.onrender.com/payment/success/{transaction_id}/{user.id}/{course.id}/',
            'fail_url': 'https://online-school-project.onrender.com/payment/fail/',
            'cancel_url': 'https://online-school-project.onrender.com/payment/cancel/',
            'cus_name': user.first_name,
            'cus_email': user.email,
            'cus_phone': "01817822166",
            'cus_add1': "Madargonj",
            'cus_city': "Jamalpur",
            'cus_country': "Bangladesh",
            'product_name': course.title,
            'product_category': "Course",
            'product_profile': "general",
            'shipping_method': "NO",  
            'num_of_item': 1,       
            'product_type': "Digital" 
        }

        response = sslcz.createSession(post_body)
        
        if response.get('status') == 'SUCCESS':
            gateway_url = response['GatewayPageURL']
            
            # Return the payment URL and transaction ID
            return {
                'payment_url': gateway_url,
                'transaction_id': transaction_id
            }
        else:
            raise serializers.ValidationError("Failed to create payment session")
