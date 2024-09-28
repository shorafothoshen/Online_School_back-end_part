from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register('profile', views.UserProfileApiView, basename='profile')

urlpatterns = [
    path("register/",views.UserRegisationView.as_view(),name="regiser"),
    path("login/",views.LoginAPIView.as_view(),name="login"),
    path("", include(router.urls)),
    path('active/<uid64>/<token>/', views.activate, name = 'activate'),
    path('successful-email-verified/', views.successful, name='verified_success'),
    path('unsuccessful-email-verified/',views.unsuccessful, name='verified_unsuccess'),
    path("changeimage/",views.ProfileImageChangeView.as_view(), name="changeimage"),
    path("changepassword/",views.UserPasswordChangeApiView.as_view(),name="changepassword"),
    path("send-reset-password-email/",views.SendPasswordResetEmailApiView.as_view(), name="sendresetpasswordemail"),
    path("reset-password/<uid>/<token>/",views.UserPasswordResetApiView.as_view(), name="resetPassword"),
    path("logout/",views.LogoutAPIView.as_view(),name="logout"),
]
