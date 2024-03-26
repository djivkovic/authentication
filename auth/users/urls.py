from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, VerificationView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('user', UserView.as_view()),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
]
