from django.contrib.auth import views
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.contrib.auth import views as auth_views
from poll.views import add_choice, album_post, all_thumbnail, create_thumbnail, delete_comment, delete_poll, endpoll, list_by_user, login_view, poll_detail, polls_add, polls_delete, polls_list, signup, all_post, post_create_view, delete_post, AddLike, PostDetails, all_album_post, delete_album_post,compress_images,uploadImage,delete_compress_photo,polls_list,list_by_user,polls_add,polls_delete,endpoll,add_choice,poll_detail,poll_vote, result

urlpatterns = [

    path('', all_post, name='all-post'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('create-post/', post_create_view, name='create-post'),
    path('post/<int:pk>/like', AddLike, name='like'),
    path('single-post/<int:id>', PostDetails, name='single-post'),
    path('album-post/', album_post, name='album-post'),
    path('album-all-post/', all_album_post, name='album-all-post'),
    path('all-compress-image/', compress_images, name='all-compress-image'),
    path('upload-image/', uploadImage, name='upload-image'),
#     path('all-poll/', all_poll, name='all-poll'),
#     path('create/',create,name='create' ),
#     path('vote/<int:id>',vote,name='vote' ),
#     path('result/<int:id>',result,name='result' ),
    path('create-thumbnail/', create_thumbnail, name='create-thumbnail'),
    path('thumbnail', all_thumbnail, name='thumbnail'),

#     path('delete-poll/<int:id>/', delete_poll, name='delete-poll'),
    path('delete-post/<int:id>/', delete_post, name='delete-post'),
    path('delete-comment/<int:id>/', delete_comment, name='delete-comment'),
    path('delete-poll/<int:id>/', delete_poll, name='delete-poll'),
    path('delete-album-post/<int:id>/',
         delete_album_post, name='delete-album-post'),
    path('delete-compress-post/<int:id>/',
         delete_compress_photo, name='delete-compress-photo'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),

    
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
    name='password_change'),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),

    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_sent.html'),
    name='password_reset_done'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
     name='password_reset_complete'),
     
    path('list/', polls_list, name='list'),
    path('list/user/', list_by_user, name='list_by_user'),
    path('add/', polls_add, name='add'),

    path('delete/<int:poll_id>/', polls_delete, name='delete_poll'),
    path('end/<int:poll_id>/', endpoll, name='end_poll'),
    path('result/<int:poll_id>/', result, name='result'),
    path('edit/<int:poll_id>/choice/add/', add_choice, name='add_choice'),

    path('<int:poll_id>/', poll_detail, name='detail'),
    path('<int:poll_id>/vote/', poll_vote, name='vote'),

]
