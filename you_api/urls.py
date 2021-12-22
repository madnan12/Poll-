from django.urls import path
from you_api import views

urlpatterns = [
    path('', views.post_api_view),
    path('all-post-api', views.all_post_api_view),
    path('m-post-api', views.multiple_post_api),
    path('poll-post-api', views.post_poll_api),
    path('poll-vote-api/<int:id>', views.poll_vote_api),
    path('poll-vote-delete-api/<int:id>', views.poll_vote_delete_api),
    path('poll-vote-check-api/', views.poll_check_for_vote_api),
]
