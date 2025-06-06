from django.urls import path
from . import views

app_name = "posts"


urlpatterns = [
    path("createpost/", views.create_post, name="create_post"),
    # path("user_posts/", views.get_posts, name="get_posts"),
    path("like_post/<int:post_id>", views.handlelike, name="handlelike"),
    path(
        "comment/<int:post_id>/<int:parent_id>",
        views.handlecomment,
        name="handlecomment",
    ),
    path(
        "commentauthorinfo/<int:comment_id>",
        views.get_comment_author_info,
        name="commentauthorinfo",
    ),
    path("editpost/<int:post_id>", views.edit_post, name="edit_post"),
    path("star/<int:post_id>/<int:amount>", views.send_stars, name="send_stars"),
]
