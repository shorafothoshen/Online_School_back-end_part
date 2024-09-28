from django.urls import path
from .views import payment_success,payment_fail,payment_cancel,EnrollCoursePaymentView,CheckUserEnrollmentView

urlpatterns = [
    path('success/<str:trans_id>/<int:user_id>/<int:course_id>/', payment_success, name='payment_success'),
    path('fail/', payment_fail, name='payment_fail'),
    path('cancel/', payment_cancel, name='payment_cancel'),
    path('enroll/', EnrollCoursePaymentView.as_view(), name='enroll-course-payment'),
    path('check-enrollment/<int:user_id>/', CheckUserEnrollmentView.as_view(), name='check-enrollment'),
]
