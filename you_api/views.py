import re
from django.http import response
from django.http.response import JsonResponse
from .serializers import PollSerializer, PollSerializerGET, PostMediaSerializer, ChoiceSerializer, VoteSerializer
from poll.models import Choice, Poll, Post,PostMedia, Users, Vote
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import  get_object_or_404

from you_api import serializers


# Create your views here.

# @api_view(('POST',))
# def post_api_view(request):
#     user=request.user
#     content=request.data['content']
#     image=request.data['image']
#     video=request.data['video']
#     post=Post.objects.create(user=user, content=content)
#     postmedia=PostMedia.objects.create(post=post, image=image, video=video)
#     return Response('Post Created', status=status.HTTP_201_CREATED)

@api_view(['POST',])
def post_api_view(request):
    user=request.user
    content=request.data['content']
    post=Post.objects.create(user=user, content=content)
    request.data['post'] = post.id
    print(request.data['post'])
    serializer = PostMediaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response('created')
    else:
        return Response(serializer.errors)


def all_post_api_view(request):
    post=PostMedia.objects.all()
    serializer=PostMediaSerializer(post, many=True)
    return JsonResponse(serializer.data , safe=False)

@api_view(['POST',])
def multiple_post_api(request):
    user=request.user
    content=request.data['content']
    post=Post.objects.create(user=user, content=content)
    image=request.data['image']
    video=request.data['video']
    for image in request.FILES.getlist('video'):    
        postmedia = PostMedia.objects.create(
                    post=post,video=video)
    for image in request.FILES.getlist('image'):
        postmedia = PostMedia.objects.create(
                    post=post, image=image)
    return Response('created', status=status.HTTP_201_CREATED)


@api_view(['POST',])
def post_poll_api(request):
    owner=request.user
    text1=request.data.get('text')
    poll=Poll.objects.create(owner=owner, text=text1)
    choice=request.data.get('choice_text')
    # print(choice, type(choice))
    choice1=choice[1:-1].replace('"', '').split(',')
    # choice1 = [item.replace('"', '').split(',') for item in choice]

    for i in choice1:
        obj1=Choice.objects.create(poll=poll, choice_text=i)
    return Response('created', status=status.HTTP_201_CREATED)

@api_view(['POST',])
def poll_vote_api(request, id):
    poll=get_object_or_404(Poll, id=id)
    choice_id=request.data.get('choice')
    if not poll.user_can_vote(request.user):
        return Response(" you already voted for this poll!! ")
    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        vote=Vote.objects.create(user=request.user, poll=poll, choice=choice)
        return Response('Voted added', status=status.HTTP_201_CREATED)

@api_view(['POST',])
def poll_vote_delete_api(request, id=id):
    vote=get_object_or_404(Vote, id=id)
    if request.user == vote.user:
        vote.delete()
        return Response('Deleted')
    return Response('No votes belong from you !!')


@api_view(['GET',])
def poll_check_for_vote_api(request):
    profile = request.query_params.get('profile')

    poll=Poll.objects.all()
    serializer=PollSerializerGET(poll, many=True)
    return Response(serializer.data)

        