from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, VerificationView, RequestPasswordResetEmail, CompletePasswordReset, EditProfile, GetAllUsers

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('allusers', GetAllUsers.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('user', UserView.as_view()),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
    path('request-reset-link', RequestPasswordResetEmail.as_view(), name='request-password'),
    path('set-new-password/<uidb64>/<token>', CompletePasswordReset.as_view(), name='reset-user-password'),
    path('edit-profile/<uidb64>', EditProfile.as_view(), name='edit-profile')
]
