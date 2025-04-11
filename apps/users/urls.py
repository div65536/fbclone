from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("signup/", views.sign_up, name="signup"),
    path("login/", views.login_user, name="login"),
    path("home/", views.home, name="home"),
    path("logout/", views.logout_user, name="logout"),
    path("search_users/", views.search_user, name="search_users"),
    path("profile/", views.user_profile, name="profile"),
    path("getfeed/", views.get_feed, name="get_feed"),
]
