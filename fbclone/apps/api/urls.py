from django.urls import include, path
from rest_framework import routers 
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewset, basename="user")
router.register(r'posts', views.PostViewset, basename="post")

router2 = routers.DefaultRouter()
router2.register(r'comments', views.CommentViewset, basename="comment")

urlpatterns = [
    path("", include(router.urls)),
    # path("gettoken/", obtain_auth_token),
    path("registration/", views.UserRegistrationAPIView.as_view()),
    path("posts/<int:post_id>/", include(router2.urls)),
    # path("", views.user_list, name="user_list")
    path("login/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("refreshtoken/", TokenRefreshView.as_view(), name='token_refresh'),
    path("verifytoken/", TokenVerifyView.as_view(), name='token_verify'),
    path("logout/", views.Logout.as_view(), name='logout')
]

app_name = 'api'