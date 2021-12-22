from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import sys
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.utils import timezone
import secrets
import os
from django.core.files.base import ContentFile

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.base import Model
from video_encoding.fields import VideoField
from video_encoding.models import Format
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from moviepy.editor import *
from moviepy.editor import *


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password, first_name, last_name, profile_image, dob, gender, mobile_number):
        if not first_name:
            raise ValueError('Users must have an first name')
        if not last_name:
            raise ValueError('Users must have an last name')
        if not profile_image:
            raise ValueError('Users must have an profile image')
        if not dob:
            raise ValueError('Select the DOB')
        if not gender:
            raise ValueError('Select the gender')
        if not mobile_number:
            raise ValueError('Users must enter the mobile number')
        if not email:
            raise ValueError('Users must enter the mobile number')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            profile_image=profile_image,
            dob=dob,
            gender=gender,
            mobile_number=mobile_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    # Required Fields

    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # User Defined Fields
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_image = models.ImageField(
        upload_to='user_images/%Y/%m', default='media/default.png')
    dob = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, choices=gender_choices)
    mobile_number = models.CharField(max_length=20)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name',
                       'profile_image', 'dob', 'gender', 'mobile_number']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


class Post(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(Users, blank=True, related_name='like')
    dislike = models.ManyToManyField(Users, blank=True, related_name='dislike')

    def __str__(self):
        return self.content

    

class PostMedia(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/%Y/%m', blank=True, null=True)
    video = models.FileField(upload_to='post_videos', blank=True, null=True)

    # def __str__(self):
    #     return str(self.post)

    # def save(self, *args, **kwargs):

    #     if self.image:
    #         self.image = self.compressImage(self.image)
    #     super(PostMedia, self).save(*args, **kwargs)
    #     if self.video:
    #         print(self.video)
    #         clip = VideoFileClip(settings.MEDIA_ROOT+"\\"+str(self.video))
    #         videopath=settings.MEDIA_ROOT+"\\"+str(self.video)
    #         print(videopath)
    #         temp_path=videopath.split(".")[:-1]
    #         path='.'.join(temp_path)
    #         path=path+".jpg"
    #         print("join", path)
    #         frame = clip.get_frame(1)
    #         clip.save_frame(path)


    def compressImage(self, image):
        imageTemproary = Image.open(image)
        imageTemproary = imageTemproary.convert('RGB')
        outputIoStream = BytesIO()
        imageTemproary.save(outputIoStream, format='jpeg', quality=30)
        outputIoStream.seek(0)
        album_image = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % image.name.split('.')[
                                           0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return album_image




# Comments class
class Comments(models.Model):
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


class Album(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Album_post(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, default=1)
    album_image = models.ImageField(
        upload_to='album_post_images/%Y/%m', blank=False, null=True)
    album_video = models.FileField(
        upload_to='album/videos', null=True, blank=True)
    content = models.CharField(max_length=200, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.album_image:
            self.album_image = self.compressImage(self.album_image)
        super(Album_post, self).save(*args, **kwargs)

        if self.album_video:
            print(self.album_video)
            clip = VideoFileClip(settings.MEDIA_ROOT+"\\"+str(self.album_video))
            videopath=settings.MEDIA_ROOT+"\\"+str(self.album_video)
            print(videopath)
            temp_path=videopath.split(".")[:-1]
            path='.'.join(temp_path)
            path=path+".jpg"
            print("join", path)
            frame = clip.get_frame(1)
            clip.save_frame(path)


    def compressImage(self, album_image):
        imageTemproary = Image.open(album_image)
        imageTemproary = imageTemproary.convert('RGB')
        outputIoStream = BytesIO()
        imageTemproary.save(outputIoStream, format='jpeg', quality=30)
        outputIoStream.seek(0)
        album_image = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % album_image.name.split('.')[
                                           0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return album_image


class Upload(models.Model):
    nameImage = models.CharField(max_length=140, blank=False, null=True)
    uploadedImage = models.ImageField(
        upload_to='Upload/', blank=False, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.uploadedImage = self.compressImage(self.uploadedImage)
        super(Upload, self).save(*args, **kwargs)

    def compressImage(self, uploadedImage):
        imageTemproary = Image.open(uploadedImage)
        imageTemproary = imageTemproary.convert('RGB')
        outputIoStream = BytesIO()
        imageTemproary.save(outputIoStream, format='jpeg', quality=30)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % uploadedImage.name.split('.')[
                                             0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage


class Video(models.Model):
    width = models.PositiveIntegerField(editable=False, null=True)
    height = models.PositiveIntegerField(editable=False, null=True)
    duration = models.FloatField(editable=False, null=True)
    thumbnail = models.ImageField(blank=True)
    file = VideoField(width_field='width', height_field='height',
                      duration_field='duration', upload_to='compress_videos/%Y/%m')

    format_set = GenericRelation(Format)


class Poll(models.Model):
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    pub_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    def user_can_vote(self, user):
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def get_result_dict(self):
        res = []
        for choice in self.choice_set.all():
            d = {}
            alert_class = ['primary', 'secondary', 'success',
                           'danger', 'dark', 'warning', 'info']

            d['alert_class'] = secrets.choice(alert_class)
            d['text'] = choice.choice_text
            d['num_votes'] = choice.get_vote_count
            if not self.get_vote_count:
                d['percentage'] = 0
            else:
                d['percentage'] = (choice.get_vote_count /
                                   self.get_vote_count)*100

            res.append(d)
        return res

    def __str__(self):
        return self.text


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self):
        return f"{self.poll.text[:25]} - {self.choice_text[:25]}"

class Vote(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.poll.text[:15]} - {self.choice.choice_text[:15]} - {self.user.username}'
 
    




class Thumbnail(models.Model):
    video = models.FileField(upload_to='thumnail_video')

    def save(self, *args, **kwargs):
        super(Thumbnail, self).save(*args, **kwargs)
        if self.video:
            clip = VideoFileClip(settings.MEDIA_ROOT+"\\"+str(self.video))
            videopath=settings.MEDIA_ROOT+"\\"+str(self.video)
            print(videopath)
            temp_path=videopath.split(".")[:-1]
            path='.'.join(temp_path)
            path=path+".jpg"
            print("join", path)
            frame = clip.get_frame(1)
            clip.save_frame(path)