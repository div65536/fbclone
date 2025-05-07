from django.urls import include, path
from rest_framework import routers 
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewset)
router.register(r'posts', views.PostViewset)

urlpatterns = [
    path("", include(router.urls)),
    # path("", views.user_list, name="user_list")
]
