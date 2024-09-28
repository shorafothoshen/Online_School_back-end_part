from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CourseModel, EnrolledCourseModel
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from accounts.models import User
from django.http import JsonResponse
from .serializer import EnrollCoursePaymentSerializer, EnrolledCourseSerializer


class EnrollCoursePaymentView(APIView):
    serializer_class = EnrollCoursePaymentSerializer

    def post(self, request):
        # Validate and create the payment session
        serializer = self.serializer_class(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            try:
                # Call the create method from serializer, which creates the SSLCommerz payment session
                payment_data = serializer.save()
                return Response(payment_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def payment_success(request,trans_id,user_id,course_id):

    try:
        user = User.objects.get(id=user_id)
        course = CourseModel.objects.get(id=course_id)
        EnrolledCourseModel.objects.create(
            user=user,
            course=course, 
            enroll_date=timezone.now(),
            transaction_id=trans_id,
        )
        # Find the enrolled course using the transaction_id
        enrolled_course = EnrolledCourseModel.objects.get(transaction_id=trans_id)
        enrolled_course.payment_status = 'SUCCESS'  # Assuming you have a field for payment status
        enrolled_course.save()

        email_subject = "Payment Successfully!!"
        email_body = render_to_string('payment_successfully_email.html', {
            "user":f'{user.first_name} {user.last_name}',
            "course":course.title,
            "course_amount":course.amount,
            "transection_id":trans_id,
        })
        email = EmailMultiAlternatives(email_subject , '', to=[user.email])
        email.attach_alternative(email_body, "text/html")
        email.send()

        # Optionally: Redirect to a success page or enroll the user
        return render(request, 'payment_success.html',{
            "user":f'{user.first_name} {user.last_name}',
            "user_email":user.email,
            "course":course.title,
            "course_amount":course.amount,
        })
    except EnrolledCourseModel.DoesNotExist:
        return JsonResponse({'error': 'Invalid transaction ID'}, status=404)


@csrf_exempt
def payment_fail(request):
   
    return render(request, 'payment_fail.html')

@csrf_exempt
def payment_cancel(request):
   
    return render(request, 'payment_cancel.html')

class CheckUserEnrollmentView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
            enrollments = EnrolledCourseModel.objects.filter(user=user)
            if enrollments.exists():
                serializer = EnrolledCourseSerializer(enrollments, many=True)

                return Response({
                    "enrolled": True,
                    "message": "User is enrolled in courses.",
                    "courses": serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "enrolled": False,
                    "message": "User is not enrolled in any course."
                }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
