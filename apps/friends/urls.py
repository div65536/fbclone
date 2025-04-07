from django.urls import path
from . import views 

app_name = 'friends'

urlpatterns = [
    path('sendrequest/',views.send_request,name='send_request'),
    path('get_requests/',views.get_requests,name='get_requests'),
    path('get_friends/',views.get_friends,name='get_friends')
]
