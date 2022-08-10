from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserResetPasswordView, UserPasswordResetDoneView,
    UserPasswordResetConfirmView, UserPasswordResetCompleteView,
    RegisterView,
)



app_name = 'accounts'
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('reset/', UserResetPasswordView.as_view(), name='reset_password'),
    path('reset-done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('confirm/complete', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
