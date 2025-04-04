from django.urls import path
from . import views 

urlpatterns = [
    path('createpost/',views.create_post,name='create_post'),
    path('user_posts/',views.get_posts,name='get_posts'),
]
