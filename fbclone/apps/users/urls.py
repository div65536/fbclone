from django.urls import path
from users import views
from django.contrib.auth import views as auth_views

app_name = "users"

urlpatterns = [
    path("signup/", views.sign_up, name="signup"),
    path("login/", views.login_user, name="login"),
    path("home/", views.home, name="home"),
    path("logout/", views.logout_user, name="logout"),
    path("search_users/", views.search_user, name="search_users"),
    path("profile/", views.user_profile, name="profile"),
    # path("getfeed/", views.get_feed, name="get_feed"),
    path("profile/",views.get_profile, name="get_profile"),
    path("upload_profile_picture/",views.upload_profile_picture,name="upload_profile_picture"),
    path("upload_cover_picture/", views.upload_cover_picture, name="upload_cover_picture"),
    path("upload_bio/", views.upload_bio, name="upload_bio"),
    path("buy_diamonds", views.buy_diamonds, name="buy_diamonds"),
    path("", views.HomePageView.as_view(), name='home'),
    path("config/", views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('success/', views.SuccessView.as_view()), # new
    path('cancelled/', views.CancelledView.as_view()),
]