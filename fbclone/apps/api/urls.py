from django.urls import include, path
from rest_framework import routers 
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'users', views.UserViewset, basename="user")
router.register(r'posts', views.PostViewset, basename="post")

router2 = routers.DefaultRouter()
router2.register(r'comments', views.CommentViewset, basename="comment")

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
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