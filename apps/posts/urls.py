from django.urls import path
from . import views

app_name = "posts"


urlpatterns = [
    path("createpost/", views.create_post, name="create_post"),
    path("user_posts/", views.get_posts, name="get_posts"),
    path("like_post/<int:post_id>", views.handlelike, name="handlelike"),
    path("comment/<int:post_id>",views.handlecomment,name="handlecomment"),
]
