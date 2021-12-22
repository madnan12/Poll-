from django.contrib import admin
from .models import Album, Album_post, Comments, Thumbnail, Users, Post, PostMedia, Upload,Poll,Choice,Vote
from django.contrib import admin
# from video_encoding.admin import FormatInline
from django.contrib import admin
from video_encoding.admin import FormatInline
from .models import Video
# Register your models here.

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display=['username','first_name', 'last_name','profile_image','dob', 'mobile_number','gender']
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=[ 'content','user']
@admin.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):
    list_display=['post', 'image','video']

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display=['user', 'post','comment', 'created_at']

@admin.register(Album_post)
class AlbumPostAdmin(admin.ModelAdmin):
    list_display=['content','album_image', 'album_video']

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display=['name','created_at']

@admin.register(Upload)
class PhotoAdmin(admin.ModelAdmin):
    list_display=['nameImage','uploadedImage']


admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Vote)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
   inlines = (FormatInline,)

   list_dispaly = ('get_filename', 'width', 'height', 'duration')
   fields = ('file', 'width', 'height', 'duration')
   readonly_fields = ( 'width', 'height', 'duration')

admin.site.register(Thumbnail)
