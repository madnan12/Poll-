from re import search
from django.conf import settings
from django.db import models
from django.db.models import fields
from django.http import request
from poll.models import Post,PostMedia,Poll,Choice, Users,Vote
from rest_framework import serializers
from youonline.settings import SITE_NAME
from rest_framework.response import Response

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields='__all__'

class PostMediaSerializer(serializers.ModelSerializer):
    # post=PostSerializer()
    # image=serializers.ImageField(required=False)
    # video=serializers.FileField(required=False)

    # image= serializers.SerializerMethodField()
    # video= serializers.SerializerMethodField()

    class Meta:
        model=PostMedia
        fields=['post', 'video', 'image']
        # extra_kwargs = {
            
        #     'image': {'required': False, 'allow_blank':True},
            
        # }
        # extra_kwargs={'video': {'required': False, 'allow_blank':True}}

    def to_representation(self, obj):
        if obj.image:
            request = self.context.get('request')
            image_url = f"{SITE_NAME}{obj.image.url}"
            return image_url
        else:
            request = self.context.get('request')
            video_url = f"{SITE_NAME}{obj.video.url}"
            return video_url
            


    # def get_image(self, obj):
    #     request = self.context.get('request')
    #     image_url = obj.image.url
    #     return settings.MEDIA_ROOT+"\\" +request.build_absolute_uri (image_url)

    # def get_video(self, obj):
    #     request = self.context.get('request')
    #     video_url = obj.video.url
    #     return settings.MEDIA_ROOT+"\\" +request.build_absolute_uri (video_url)
    # def get_image_url(request, path):
    #     url = request.scheme + ":\\" + request.get_host() + path
    #     return url
        

     # def get_image(self, obj):
    #     request = self.context.get('request')
    #     image_url = obj.image.url
    #     return settings.MEDIA_ROOT+"/"+(image_url)

    # def get_video(self, obj):
    #     request = self.context.get('request')
    #     video_url = obj.video.url
    #     return settings.MEDIA_ROOT+(video_url)
  
    # def get_image(self, obj):
    #     return '%s%s' % (SITE_NAME, obj.image.url)

    # def get_video(self, obj):
    #     return '%s%s' % (SITE_NAME,  obj.video.url)


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model=Poll
        fields=['id','owner', 'text']


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Choice
        fields=['poll', 'choice_text']

    
class VoteSerializer(serializers.ModelSerializer):
 
    class Meta:
        model=Vote
        fields=['user', 'poll', 'choice']


class PollSerializerGET(serializers.ModelSerializer):
    # poll_choices=ChoiceSerializer(many=True)
    choice=serializers.SerializerMethodField()
    voted=serializers.SerializerMethodField()
    class Meta:
        model=Poll
        fields=['id','owner', 'text', 'choice','voted']
    
    def get_choice(self, value):
        choices= Choice.objects.filter(poll=value)
        serializer=ChoiceSerializer(choices, many=True)
        return serializer.data

    def get_voted(self, value):
        vote=Vote.objects.filter(poll=value)
        # serializer=VoteSerializer(vote, many=True)
        # return serializer.data
        if vote:
            return True
        return False




