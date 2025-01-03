
from django.urls import path
# from .views import (UserRegistrationView,
#                     # LoginTokenGenerate,
#                     UserLogoutView,
# LoginLogoutView
#                     )
from .views import (user_logout, user_registration,login)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# urlpatterns = [
#     path('register/', UserRegistration.as_view(), name='register'),
#     path('login/', LoginLogoutView.as_view(), name='token_obtain_pair'),
#     path('logout/', UserLogoutView.as_view(), name='logout'),
# ]
urlpatterns = [
    path('register/', user_registration, name='register'),
    path('login/', login, name='token_obtain_pair'),
    path('logout/', user_logout, name='logout'),
]