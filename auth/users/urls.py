from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, VerificationView, RequestPasswordResetEmail, CompletePasswordReset, EditProfile, GetAllUsers, CreateContract, AcceptContract, RejectContract, GetAllContracts, GetAllAcceptedContracts, MakeReservation, CancelReservation

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('allusers', GetAllUsers.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('user', UserView.as_view()),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
    path('request-reset-link', RequestPasswordResetEmail.as_view(), name='request-password'),
    path('set-new-password/<uidb64>/<token>', CompletePasswordReset.as_view(), name='reset-user-password'),
    path('edit-profile/<uidb64>', EditProfile.as_view(), name='edit-profile'),
    path('create-contract', CreateContract.as_view(), name="create-contract"),
    path('accept-contract/<int:contract_id>', AcceptContract.as_view(), name="accept-contract"),
    path('reject-contract/<int:contract_id>', RejectContract.as_view(), name="reject-contract"),
    path('get-all-contracts', GetAllContracts.as_view(), name='get-all-contracts'),
    path('get-accepted-contracts', GetAllAcceptedContracts.as_view(), name='get-accepted-contracts-view'),
    path('make-reservation', MakeReservation.as_view(), name='make-reservation-view'),
    path('cancel-reservation', CancelReservation.as_view(), name='cancel-reservation-view')
    
]
